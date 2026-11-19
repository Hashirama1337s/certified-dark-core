"""lincore.py - coefficient jets of the linearised GPP operators from a certified background tube, and a marcher
that runs itaylor.lin_step along the tube's own step grid (outward or inward, with a split at the end radius).

Coefficient names (all jets are rigorous enclosures; 'pt' = about the step base point, 'box' = over the step box):
  sig   sigma            sig2  sigma^2          u     u            ir2   1/r^2         rsig  r sigma
"""
from flint import arb, ctx
import itaylor as it


class BgJets:
    def __init__(self, s, steps, Yend, Kl, prec=None):
        self.s = s
        self.steps = steps
        self.Yend = Yend
        self.Kl = Kl
        self.prec = prec
        self._pt = {}
        self._box = {}
        self.r = [st['r'] for st in steps] + [steps[-1]['r'] + steps[-1]['h']]

    def _derive(self, rc, J, n):
        S, P, U = J[0], J[1], J[2]
        S = S[:n + 1]; U = U[:n + 1]
        sig2 = [it.conv(S, S, k) for k in range(n + 1)]
        ir2 = it.inv_r2_jet(rc, n)
        r1 = it.r1_jet(rc, n)
        rsig = [it.conv(r1, S, k) for k in range(n + 1)]
        return dict(sig=S, sig2=sig2, u=U, ir2=ir2, rsig=rsig)

    def pt(self, i):
        """jets about r_i (i = 0..len(steps)); i = len(steps) is the tube end."""
        if i not in self._pt:
            n = self.Kl + 1
            if i < len(self.steps):
                rc = self.steps[i]['r']; Y = self.steps[i]['Y']
            else:
                rc = self.r[-1]; Y = self.Yend
            J = it.bg_jets(self.s, rc, Y, n)
            self._pt[i] = self._derive(rc, J, n)
        return self._pt[i]

    def box(self, i):
        if i not in self._box:
            n = self.Kl + 1
            st = self.steps[i]
            rI = st['r'] + it.tball(st['h'])
            J = it.bg_jets(self.s, rI, st['B'], n)
            self._box[i] = self._derive(rI, J, n)
        return self._box[i]

    def index_of(self, r):
        """largest i with r_i <= r (float compare on midpoints)."""
        rf = float(arb(r).mid())
        lo, hi = 0, len(self.r) - 1
        while lo < hi:
            m = (lo + hi + 1) // 2
            if float(self.r[m].mid()) <= rf + 1e-15:
                lo = m
            else:
                hi = m - 1
        return lo


def scaled(jets, terms):
    """build a dict of combined jets: terms = {newname: [(name, scale), ...]} (scale arb/int; name 'one' = 1)."""
    out = dict(jets)
    n = len(jets['sig'])
    z = jets['sig'][0] * 0
    for nm, lst in terms.items():
        acc = [z] * n
        for (name, sc) in lst:
            if name == 'one':
                src = [z + 1] + [z] * (n - 1)
            else:
                src = jets[name]
            acc = [acc[k] + src[k] * sc for k in range(n)]
        out[nm] = acc
    return out


def march(sysd, bj, X0, r_from, r_to, K, terms=None, on_step=None):
    """integrate the LinSys sysd from r_from to r_to along the tube grid. r_from must be a grid point.
    terms: combined coefficient jets to build per step (see scaled). on_step(rc, h, C, R, X0, X1)."""
    out = r_to > r_from if isinstance(r_to, (int, float)) else float(arb(r_to).mid()) > float(arb(r_from).mid())
    rt = arb(r_to)
    i = bj.index_of(r_from)
    assert abs(float((bj.r[i] - arb(r_from)).mid())) < 1e-14, 'r_from must be a grid point'
    X = X0
    nst = 0
    pos = bj.r[i]
    if out:
        while True:
            rc = bj.r[i]
            if float(rc.mid()) >= float(rt.mid()) - 1e-15:
                break
            h = bj.steps[i]['h']
            if float((rc + h).mid()) > float(rt.mid()) + 1e-15:
                h = rt - rc
            pos = rc + h
            jp = bj.pt(i); jb = bj.box(i)
            if terms:
                jp = scaled(jp, terms); jb = scaled(jb, terms)
            X1, C, R, B = it.lin_step(sysd, jp, jb, X, h, K)
            if on_step:
                on_step(rc, h, C, R, X, X1)
            X = X1
            i += 1
            nst += 1
            if float((rc + h).mid()) >= float(rt.mid()) - 1e-15:
                break
    else:
        # inward: from grid point r_i down to rt
        while True:
            rc = bj.r[i]
            if float(rc.mid()) <= float(rt.mid()) + 1e-15:
                break
            h = -bj.steps[i - 1]['h']
            if float((rc + h).mid()) < float(rt.mid()) - 1e-15:
                h = rt - rc
            pos = rc + h
            jp = bj.pt(i); jb = bj.box(i - 1)
            if terms:
                jp = scaled(jp, terms); jb = scaled(jb, terms)
            X1, C, R, B = it.lin_step(sysd, jp, jb, X, h, K)
            if on_step:
                on_step(rc, h, C, R, X, X1)
            X = X1
            i -= 1
            nst += 1
            if float((rc + h).mid()) <= float(rt.mid()) + 1e-15:
                break
    # the float compares above only steer; the end point actually reached must enclose r_to (no snap across a gap)
    if not (pos - rt).contains(0):
        raise RuntimeError('march: reached r=%s, not r_to=%s (a grid point within 1e-15 of r_to)' % (pos, rt))
    return X, nst
