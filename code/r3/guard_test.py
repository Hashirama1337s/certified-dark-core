"""guard_test.py - checks the assemble_w seal guard WITHOUT touching the window: N:/C: jobs with tags that have no
SEALED-<tag>.ok file must exit 2 and print REFUSED before any computation. Tags used: n1500 (sigma0 = 3/2, outside the
window, not a schedule node) and c99 (no such cell). Neither file exists (asserted)."""
import os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
MC = [sys.executable, '-B']
ok = True
for tag, job in (('n1500', 'N:n1500'), ('c99', 'C:c99')):
    assert not os.path.exists(os.path.join(HERE, 'SEALED-%s.ok' % tag))
    p = subprocess.run(MC + [os.path.join(HERE, 'assemble_w.py'), job], capture_output=True, text=True, timeout=120)
    out = p.stdout.strip().splitlines()
    refused = any(l.startswith('REFUSED') for l in out)
    # memcap passes the child's exit code through ("memcap: exit 2")
    code2 = any('exit 2' in l for l in out + p.stderr.strip().splitlines()) or p.returncode == 2
    print('%s -> returncode %d, refused %s, exit-2 %s | %s' % (job, p.returncode, refused, code2, ' / '.join(out)))
    ok = ok and refused and code2
print('GUARD TEST', 'PASS' if ok else 'FAIL')
sys.exit(0 if ok else 1)
