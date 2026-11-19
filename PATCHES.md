# PATCHES: what was changed in the shipped copies, and why

**In plain words.** The lab's files name folders on the lab machine, and two of them mention a person. To keep machine
paths and personal names out of a public repository, every shipped copy had those strings replaced by fixed
placeholders from one table (part A). Nothing else in any file was changed: no number, no line of logic. Part B points
to the instrument changes between the R1 and R2 runs, which are lab history, not edits made for this release.

## A. Substitutions in the shipped copies

Applied in this order (S1 first). In code, each lab folder became the repository-relative folder where the same files
now live, so the scripts run from the repository root (see reproduce.md). In documents, folders became placeholders.
The original strings are not stored here, in any encoding. The **original sha256** of each patched file is listed, so
the lab can show that its unpatched file is the one that was sealed, run or pinned.

| entry | replaced by | what the original named |
|---|---|---|
| S1 | `python -B checks/` | the lab's memory-cap launcher prefix in the check scripts' usage lines |
| S2 | `python` | the lab's memory-cap launcher (usage lines, run notes) |
| S3 | `<MEMCAP>` | the lab's memory-cap launcher (other mentions) |
| S4 | `data/r1/` | the R1 output folder (code literals) |
| S5 | `code/r1` | the R1 instrument folder (code literals) |
| S6 | `data/blind/` | the blind seat's data files (code literals) |
| S7 | `code/blind` | the blind seat's code folder (sys.path lines) |
| S8 | `data/band-map/` | the float map's data files (code literals) |
| S9 | `code/band-map` | the float map's code folder (sys.path lines) |
| S10 | `code/r1/` | the R1 instrument folder, Windows form (the "wrote" line of each run log) |
| S16 | `code/r2/` | the R2 instrument folder, Windows form (the "wrote" line of each R2 run log) |
| S11 | `<LAB>/` | the lab project folder (documents) |
| S12 | `<LAB-ROOT>/` | the lab hunt folder (documents) |
| S13 | `<TOOLS>/` | the lab's tool folder (documents) |
| S14 | ``<a session transcript folder>`` | a folder in the operator's user profile (blind-seat RESULT.md, one mention) |
| S15 | `The owner said "Yes, finish it"` | the lab owner's first name (BAR-R1-BLIND.md, one mention) |

Two of these replacements are not paths:
- S14 replaces a folder of the operator's user profile mentioned once by the blind seat (it reports that a guard
  refused a read there, and that nothing was read).
- S15 replaces the lab owner's first name in one sentence of BAR-R1-BLIND.md (the owner's go-ahead for the blind
  seat). The sealed meaning is unchanged.

**Sealed files.** Four shipped files under `seals/` are sealed texts. Their shipped copies differ from the sealed bytes
only by the substitutions listed; the original sha256 column equals the sha256 recorded when each was sealed
(BAR-R1-FINAL 70ef9b9e..., AMENDMENT-R1-1 c0cb5b42..., BAR-R1-BLIND 97c1c3c6..., BAR-R2-EDGES 21122fca...).

**Run logs.** In each `data/r1/*.log` and `data/r1/cal/*.log` the one line `wrote <folder>\<file>.json wall N s`
had its lab folder replaced (S10); the same for the R2 logs in `data/r2/logs/` (S16). No other line of any log, and no
JSON output, contained a local path.

**Unpatched copies.** Every other shipped file from the lab (all instruments in `code/r1/` and `code/r2/`, every
JSON output, the float-map data) is a byte-identical copy.

## Patched files

| file | original sha256 | shipped sha256 | entries |
|---|---|---|---|
| code/blind/spec.py | `5ae9b79ad545376ab97c47ad89f93848e483e2dbd23d1d0abc48a6faed8409fb` | `0a8e65d09393ce7cde3334121a435f8f7f02a31b1f487b49aebf081c4d1032f6` | S7 x1 |
| code/blind/run_main.py | `b67da7cef5f30f1f49b1b85cc64bb2d82d45de5307da3eea86864b8ea6e7c777` | `b00ced38bb115ab7a286b291e65d92dceead32b5fe84c0a9da28095bbd018417` | S6 x1, S7 x1 |
| code/blind/assemble.py | `e8d46eceec049975df338144973e04f8e2aa1a42540b7cef644f1ca12027783a` | `2c3f91fc36f74c687513acde7a26faabe7e08a3fe3431eb01afe7b2a55326158` | S6 x1 |
| code/blind/ctrl_bg.py | `ec1889e18879e64dfb05c808c05579b743fb6da8012840201306a626694f1fb5` | `d7d7175fffa2f37237f5daca7f59fb2cb9a44a462a124739290a222f4a8f728c` | S7 x1 |
| code/blind/ctrl_spec.py | `17752a65734b6391498c1d3006559f520d72066941fbbd950206e2a55bb14665` | `b867de93fefc8537d33690c05911b89639ebc1e5e5b3ffb31cbbbf1973238676` | S6 x1, S7 x1 |
| code/blind/probe_bg.py | `2e0e439f604a26a715b48c99ae93dfeedf18c617e0d908d08eab731cb1c29b06` | `a3fecd35f5f1ca1291789a676b69e20473a0b7cb9aa46d8256f81238cae99149` | S7 x1 |
| code/blind/probe_one.py | `ab355a0ee1fea9f2ca3119ad893ef0e96fae6750bac8728d9b8ca87faace6430` | `a72f0ca5efab19abf966126d3c50be94e790e7018baa3550c95309487b6c9b0d` | S7 x1 |
| code/blind/RUN.md | `72d6b930c2da1ebf049760bada8b89a2f0259089df766cff1b8cc133aca19cf0` | `5899385c9253ba0f1f4913113ba3cc4e6c429682adc7cb021b9d9cb3f639222a` | S2 x1, S7 x1 |
| data/blind/RESULT.md | `2ceff248c3342ee758589fefe4ba07b21bc8c46643c3cd768bd7acc6f682eecf` | `ef9c470d76b40f175232180d7a9cbb4fd8e556f9f5d393f244cb760f39c56d2c` | S6 x1, S14 x1 |
| checks/check_U0.py | `e5bb36e0456591caa37c7b0ce5813fa79b2a97a19962350fbdba0f00aa17727e` | `b1521e574ef2b411d00de81b4967bb246f067a7674e4003953588a62fefc7af1` | S1 x1, S4 x1, S5 x1 |
| checks/check_assembly.py | `8bfa41f63a58b8b6aa90a5f88850211739b882d2e203dc317be27e84685bc1c0` | `8fe1d53eefb90d689f71d5522f2f5dd67f26fd4a92006668212115d36fe2e45b` | S1 x1, S4 x1 |
| checks/check_frob_slack.py | `ee17f45fae4f7f90dc7717983d730a2395f2c2979237c31036f7f7a946acb5f4` | `a3918212e269bb8f80b2562d9766ce633b14c37f01e3975a9802b354c44f1427` | S1 x1, S5 x1 |
| data/r1/target-B.log | `0c043bb9a3eff1dc34877466a105876b9b20ee745b90238c1e3a62644fe7908d` | `6e88669e0803e54142821b148f0f7d1ec818b5fcec2242c3dfadded68b51ef8d` | S10 x1 |
| data/r1/target-K0.log | `6814f2f461e596b7d0a706cc25b9699105a9b45b969ce06f6cd064accd1c24f1` | `ee549deba7e4a12dc267031bf65e9e59894a66f374327fc8ae8f16a14a287615` | S10 x1 |
| data/r1/target-K1.log | `d942fbe8db64adc612d7a4115d9aa337b98fc8678d678f6a30053102fd1ff847` | `653ecd5f6078450465f0576c3fdc5c167727f5eebe2d2b5be96774fcab1125db` | S10 x1 |
| data/r1/target-K2.log | `c7fa5d584d0eb8d5f8c8cd68140ea7de73132618bf2ec3170658672e836b5f88` | `972595de9ff865fc683eacac6ee49a1d57327427056051263912884bc387301b` | S10 x1 |
| data/r1/cal/C-B1.log | `3c93f1edce5006031bd72ddd6af57612059294d1d761107ddb6dc556bec2559b` | `d6d6c522d3a844bf9a60dbbd526ee11334a9eaa51e9d099e9fcb4513276d6ad0` | S10 x1 |
| data/r1/cal/C-B2.log | `39553357c649a8c1fb6550f0ce82b89d2f090a3501ab6faca9fd5684f6d569ed` | `1303eaf8d8e74e70b418740c92740e03882ca8e6f48f6909325c8c14aee00bd0` | S10 x1 |
| data/r1/cal/C-P1.log | `2836237d17528223d7638121cf34c0b8d8938052e8f81bcc20044cade28027f0` | `b0fec214b88e0ce10da1c2ffae3434855118af67f846631f0ea89d887cbbf177` | S10 x1 |
| data/r1/cal/C-P2.log | `803eee8f6c57865a8a7c4d25c1f920a1469ff3cb58904a176d88d03f3084f77f` | `47cc027274a4678c669fc0f7600184761907b6ee54d3315eeaf4088f058f6cec` | S10 x1 |
| data/r1/cal/C-P3.log | `ec99dce1b1175ae00eb83dafb0efd6036e121397ef1c1549f1090742260e493e` | `5cba45bb1b52f99e61e27c00cff7693e9582dedc5322cb4e55e19187b294aa84` | S10 x1 |
| data/r1/cal/CAL-K.log | `8ce2d15914efe4cfe02a74dc1033d8028e1adab4b8836f4d53970862309db25d` | `33fc5a91a952cf904ff9336040d374b20737487c37bebe726a833aa2e758c425` | S10 x1 |
| data/r1/cal/NULL.log | `0f9f26f4c25097c9b4342732d973d2b0c5bf591f65cb858569a46d4619c58afd` | `7cbf0f1419ce55ac264f40045188d697690322458484b36c0959d59d01c25362` | S10 x1 |
| data/band-map/MAP.md | `f75a64bb0fbed73cef6e6f52d36966eb65583a04e3dd299f008ad642b467432a` | `1ae0fdeb0f38001190bccd5f71234a3344ac1ada4a1f5c1ee4f866ac23110ff9` | S2 x1, S8 x1 |
| code/band-map/lite.py | `29362b11dd3a4997e1f4fb73f1ecaa070f57c179b8d81684ec5629db184e68cc` | `16ce37c99052d9ffeaf89b63edb1ac784831ac0639601814910e93819a9ef649` | S9 x1 |
| code/band-map/sweep.py | `994bad5edb2fe476d4dc24db3531ac1cb933af185932ccd7fdf3ef4e71470fdb` | `f2ba529da984b93a474f88c47ebea11e352b8fc041798b689e1dc034760f2966` | S8 x1, S9 x1 |
| code/band-map/edge.py | `2a8c71155f350f628005cfcb48bd9b5760d3465574c38b352911211ab3da3750` | `40292fc54d43353388769c3296cf52656cef9c6602b26eeaf3153c2e88100af9` | S8 x1, S9 x1 |
| code/band-map/check.py | `77170422720f82dd1f6c8c965f8fbdc62cbd067f6ba2811af156accd0690515a` | `a25f216c7bfb7c6e3ad47ceca971a5a39f80b394722742a30f7b14d50163e7b4` | S8 x1, S9 x1 |
| code/band-map/analyze.py | `1edd10e85f6753274e2df948194e69e9bb5b2804791ab6fd1d191260cf05d61d` | `5cc91b939530472b62a8b6fa4d6cfbfed1a4b96ee6c44ddc548aba404b2a273a` | S8 x1 |
| seals/BAR-R1-FINAL.md | `70ef9b9eaea7e45926e789b0c4100f9889e4e2648d1e19c042046c8a2f40ec8e` | `72604ad3e57c2f3f66355d5e9c848f109e38301772003816acafc7aa58c4d450` | S11 x1, S12 x3 |
| seals/AMENDMENT-R1-1.md | `c0cb5b42f3ffc26380ce1daa9b6963b580f24a471f39e57b86e178200d354204` | `e6f216dd58aee21ca8473f3291ee4134640c7ae2e2693c5afd5dbdeb5b37548b` | S5 x2, S11 x2 |
| seals/BAR-R1-BLIND.md | `97c1c3c6a4cd1cbb33e7af4615023b98a063490ff8ae500c6ccef15883a4989e` | `31a8675bb2868197adc60b30c488c09894dbae948f28d8a6de6b8efe8e1aaa88` | S12 x1, S15 x1 |
| seals/BAR-R2-EDGES.md | `21122fcaa3fa3c4519fbf4dd1485deed46c2e841311bb399370236fccf66f884` | `7ef0a1e05ced27d78b553cf65386e28cc4a462676c041d0c06ac949fece31a50` | S11 x2 |
| proof/PROOF-R1-v2.md | `518ff9ff8679988fad7027eecc0898791f4aaf0109b088cc0f18f38a51d9f72c` | `5b54fec65b1f49ca280664fa67ebc6bf9cda5379093ba515c6f804789673e493` | S12 x1 |
| data/r2/logs/B_g165.log | `ee3611b229196c1291484e9e42cbb5c9ccffa3d5b632a8111c4e962fdac27d97` | `dc1f8545b7eb52e8c8d453bf607aa50bb17c37f1ef8e5c5e44df2afe390b35c4` | S16 x1 |
| data/r2/logs/B_g170.log | `c00df26f256b0fa1d69e8f9209e046ff853b9cabb2679f7d1acbda1440e71e59` | `6404317e5cfd77bf362a149cd3ca491d278f640fdb17a52aab9e05839a009a47` | S16 x1 |
| data/r2/logs/B_g175.log | `aa751b086b464509d909e1d9bdb548686cac3fc38e018441966f501ee309653d` | `7f2ab92ab953ac9a76c8979337f5543134141174c3ac138d9c666191c9c06356` | S16 x1 |
| data/r2/logs/B_g185.log | `3c03eb5709ff55949a078995d7884a13cf9e1d159ccef4bd6db6d0d4158b868b` | `9014a4a95ffb1595bd6c7611cca40e83561be26bf1f771acea1499337f63face` | S16 x1 |
| data/r2/logs/B_g190.log | `603c300d7907ac5de466664e9ab84db6c480848561b389999ce067d35ccf3334` | `99b9a8a4587c3a33ef70b06d19226989791e9ef21a81af482703a66cfaf80821` | S16 x1 |
| data/r2/logs/B_g195.log | `ceb1297ee8df9e12b04040c8471ce64fb5db258c49877199120d496329ddb9e1` | `f20e6b698241743a0f17db0088f2db83b42eab04d2f2da511074aa1c2210a403` | S16 x1 |
| data/r2/logs/B_hi-s.log | `73866c944dbc8901829e08cdaf342ab362a2ac267d578a73a23ea7f12a089fb1` | `d8f85ed38ff33923dbe3dd4be21f332b370b07c4d7e29ea0c848d4a71543474c` | S16 x1 |
| data/r2/logs/B_lo-s.log | `5c5e65edbbdc8cd5b7b0182991217ceb79324dc23cfa59d0551d0be93c7a85b9` | `02aaa617ae74c4fa0ef23ea1475389c4c6e495d86638f576715d66dc8d2b70b4` | S16 x1 |
| data/r2/logs/B_p161.log | `c0f8946c6aa08e1f46ab3bee5e7d68dcdf9fa2922cd8aa3af132c76613812c11` | `aa56a5fb302df943ebc02874ea4baae1b3c9c1f708f05478a28849831734b265` | S16 x1 |
| data/r2/logs/B_r1.log | `91ead5e26fd76ed35dc3466f6350b3dd364726e77eb306ea94da59a36cbd84b3` | `53a90b4bc11de37a75b8d79b97aa4f535d738d7b43d85731e8f3716206208dd8` | S16 x1 |
| data/r2/logs/C-B1.log | `f79e39c31f8a78777a34863b43e20227187eb22d29c578962ac9894af97087e0` | `7755e5327d9d213d94b303dade458f5cbdfd8bb6ce9b1cf2fbb231357eb5f5a6` | S16 x1 |
| data/r2/logs/C-B2.log | `61e263c47d74ed4fb4615c9fdce208e0f45292830baf6f18db2a540bcaf9401f` | `ecb95ad12eaaaa7c0fc0e5b055376708bf62845a8181a6c258ac9c870d7b6eb9` | S16 x1 |
| data/r2/logs/C-P1.log | `4b20d3097df96876eb5a52acc1920320e2e7f336d3da117c16278385204f22a2` | `d10ca89caca07488f484f89fff78bf011075f65a82b27f99c02e001b7b9fd89f` | S16 x1 |
| data/r2/logs/C-P2.log | `01633b84a3ea21f02c8f4352bf60c626e8dbd50fc701250364839e5b28ebdc69` | `f9cb751af4b562ef16a0bf50199b80de3e71a3e70eadb6cea5bc406f9f2e99ca` | S16 x1 |
| data/r2/logs/C-P3.log | `0cec853eecf9f846896bb16e1c8b48233dfee4887d39fcd5b536bb277bdf61ca` | `ccdd4522a60fa6751cef0b4f398f5fbd131e82376968d85e5406e8534bc96a1f` | S16 x1 |
| data/r2/logs/CAL-ED.log | `8e6c88bd058796890cdac2e579fd7213d18efb2e20e0d47303bce7864e983f07` | `72c4c7f9af4ceba59316ff6468d9c983f8315381ba7717a133a48dcb5934f482` | S16 x1 |
| data/r2/logs/CAL-K.log | `3363c9e707b686d9ecb80a8f9ccd5425cdfcf2a4b3fd5d0be6dea1504d66ae7b` | `e181db234a89946817ea8f72a37949cdd55cba3868556a9844960452b53d46bd` | S16 x1 |
| data/r2/logs/CAL-KD.log | `f56774f8f11c073ee8ced5526594123ebf93fd39928f8c6040d7564529a8e2f4` | `3ad5c331730095a942dd5b20b6ec02015024bb987073ef5894077a48a70e7897` | S16 x1 |
| data/r2/logs/K0_g165.log | `df48950384ffc90bf88774baae98198ea248f3f3318f583575fd8ff21c4c436c` | `142346794fb40679372cc6904cfda82264f0b66db9b0a3415d17bc76ca927675` | S16 x1 |
| data/r2/logs/K0_g170.log | `eeb6a6bc7d8c40bc077f1d010195c0e0a6522f7c805260a8c0d0f7184ee9f7ea` | `cd3d0d0c0abc3f912aecf941c864020446462e20d9b1aa9f04472eb2df4e73dd` | S16 x1 |
| data/r2/logs/K0_g175.log | `1549807cf8860f911b2d1b80d8322ec272163fa3944ad277439d595bbfc715a0` | `3555d0e39cefb53ca55f35516e4aaa2cb94db333db0c805515e9e83363d42490` | S16 x1 |
| data/r2/logs/K0_g185.log | `f59267230df8f531add15fb12b215d643ad20311414cfc7fce0eb50a1ec3117d` | `dc5cc2ff3cfe743f8c85db2e43f74e50627ec29c4ab83e74b3c5a8a49bdc3f9c` | S16 x1 |
| data/r2/logs/K0_g190.log | `358cdb7fd49a2938ff7a9699b22efe0ad484bf114c34613c2d423c8aa3a8e028` | `a63c96c050e80f82597834e78241f3a1d4a69c75d4d6943537d8cc3d0a8eb1d2` | S16 x1 |
| data/r2/logs/K0_g195.log | `d3a303aee13044bc0f5ec61d75ff4b7e1940206d105810357708004791c12c9a` | `ad146a1ea7320419502fa46f17b3ccc047626f57281236ad31af279dfd32809e` | S16 x1 |
| data/r2/logs/K0_hi-s.log | `db53f8c6e20e8619a78333d8cee85606b04a27a4303e38c6de1f0ba5121ab41b` | `fe42b2c742c3ccbb4dcc7e9eef74971c65436cab8c77afd35f741e0581068a71` | S16 x1 |
| data/r2/logs/K0_lo-s.log | `625761b74dcc7686e26187942e368e9f24ff93152e66e2872b45f4af1c89baf4` | `7c1f718fc80a2c3150210264becb4986291b5b6bcec6b89d783c2c5e14ca0331` | S16 x1 |
| data/r2/logs/K0_p161.log | `4239f6fc4b34f797863558736c0d68f83abc4ee5d0299ab30ee0b01ae96fd1ef` | `acc7399daa97ea845f13d4043fdf27f632ec837690d2092cb20df7663c36c1d3` | S16 x1 |
| data/r2/logs/K0_r1.log | `f54a8f10b8e47a4829f2700880828d2e8dba769b8d52768eefcbdcc78b0779df` | `f29f13438c2ee18134c9e68df1e1ee2f85eaf7d959f56346ea1838dee03773f4` | S16 x1 |
| data/r2/logs/K1_g165.log | `243345acc6e6eafd7e2b918320e922ad5b6ce6e48609d6e09e347e2a1a287db7` | `20b3761ad2b027310decafbc23af946db6716fe7889629cd778fcc4797f46d36` | S16 x1 |
| data/r2/logs/K1_g170.log | `f2c4abee780ccaaf6cc8a2e73a5dc9296989408dc9b0429ef51d71ce1e5ac3fe` | `9ab63d24be8c06b266e6199804855235f5f0f330782ac2cdc7d739de1b87b801` | S16 x1 |
| data/r2/logs/K1_g175.log | `ee2d0bd9f1ca762d1814923f883e32b1dcdab2fb4c5879daa221d9c2da9e9eea` | `b293aabecf490e4816e12f0ea513c1b8d693793cc30d39e55e3829e579490e36` | S16 x1 |
| data/r2/logs/K1_g185.log | `83846858f4b0a7d17e7068e39e9ed4671b2e5070f2d9b522af31a6d891274dff` | `dda0991ce59221b3e1634b24492dc9125da047b07f54f7f347e77b0dbbb11333` | S16 x1 |
| data/r2/logs/K1_g190.log | `a2f241e5466821d696d6c148b96e07444049c641ffb7f2c342fa8623d87bb090` | `034e06a2e2b4375eb9d5097374649f73aa616cd805a22a01b7b564f8cc854fbe` | S16 x1 |
| data/r2/logs/K1_g195.log | `6ad6cd910f93c129f34d92afda4e79949e0119052c1e814d4f978bf92314685a` | `78f0d70d87d01121acb55b087c872e52cadd86110045f1b2428de5c3a19c44ba` | S16 x1 |
| data/r2/logs/K1_hi-s.log | `f5a9db5ceb49e4c86e0567d490eaaa127a0e7875cc83847607b1ee5541fb8d7c` | `c049b1d0cbeb6144d2f4da298ab82764cc440b9f8c4892582441be86e58e857e` | S16 x1 |
| data/r2/logs/K1_lo-s.log | `8b0cd6348b7dd71ab915c02795ba0cb6e37f85eb4c207da719e82d7cdd1ef700` | `3ab411aaf4078120794c696678c719e6c68e7da1a27b63aa78850f6b505191ae` | S16 x1 |
| data/r2/logs/K1_r1.log | `af2357759c2a1017ea992c1e948efc0caec6780aba87647cd7e86bfe866a85fd` | `358cce022f77237500eb67dd46a8e3445ffd01d018ece416f4cc00277f475815` | S16 x1 |
| data/r2/logs/K2_g165.log | `6f7a25ee7da7b134edef03194c8ea97acb7d2e6b99e0d9d367221a9d7e30bee3` | `bb1eeed2d6420b0251a92f3f82b20f7fe6960d99e8751dbe2e1cb97d247b9db4` | S16 x1 |
| data/r2/logs/K2_g170.log | `103916032f950a192b234e3a033324d4d081ded66427e2940fd0cb42a051c6bf` | `43a3af358bed03e0b6703db730105929bc9e6f75a72e6bdf25670997d90bc4f8` | S16 x1 |
| data/r2/logs/K2_g175.log | `5003cd07cfee7e61b14a80d0c9ba5ac284ce76ee8b77a92aa3b9a4b34aa08d77` | `687d2a413c19ee59bfd82dd579cb9f707184a1599f286fcf92d96ceca23b2baa` | S16 x1 |
| data/r2/logs/K2_g185.log | `51a18662d76ae0304c2254da94de1e5a7ea7f0c77c7c204cf894458c8aad2269` | `1dad574bf50855912abf76538984bb25bde39d15ae2bd4a95b4c7b3e4a3072dd` | S16 x1 |
| data/r2/logs/K2_g190.log | `1d58292fca8ca9d0759f51893b224069d770275eab635f19e912a58943c78f18` | `009cf167c26a873d39de3f1ae911b93e4de757742e92a2cd9395ba64d0b14f9b` | S16 x1 |
| data/r2/logs/K2_g195.log | `54fc49319c67df697418d7b26a1bffa8f396e1b525bbd5a25e8eaaac6b74fc12` | `bc7752a7d937b92532184c7dab0ab3729d1d7532ac21975a11df02055e7c4090` | S16 x1 |
| data/r2/logs/K2_hi-s.log | `20ae7d06ceb68f1b1183caca231d0ec1bf4a75699cc08a0ca7f874e3a74d3588` | `1b127b4967eb7cdc0f2e7841b2b35ac7aed273a7e2e3bc464a10acdc0e954b7a` | S16 x1 |
| data/r2/logs/K2_lo-s.log | `470e8bb85a8a22708847678faea301372e10678c1b25aba7a4d344a28115b446` | `2e1b09bbbb5d9e2433cb30018d8820bd0e4ec3d98b4aaa0f7bb2efc5ab6162fa` | S16 x1 |
| data/r2/logs/K2_r1.log | `66eb06f53a2e35318b1336da1a771d635f29e9107d79a77bb81c28113d20aad4` | `9a70b73931966ba66ba0e56ee4fd7a5c3f23f607b742c4bd608a47b12bcf7eb2` | S16 x1 |
| data/r2/logs/NULL.log | `fb8ab97f9042047c120b3acd6d3c8b299ae073e5588fa932276dfe3092ef00dc` | `4d934052419cf5acec7a469227f6fe5082cdac27d4f82b5ca8b01086acab1277` | S16 x1 |
| data/r2/logs/U_hi-u.log | `454cd2b925dea503121ff41b8ba38240a41242d34e6b7fbb270ebce35f92a46a` | `6cb4a8f24c53510506770a8594871971433a0052c1f98cd33cbab9835e472d1f` | S16 x1 |
| data/r2/logs/U_in-155.log | `d318fbfb0f4988547f9f45bd45aa45a554583a8c56807fab036b1b27e2044adb` | `7c9f11052bfca96be05dcf54ebb79ae5b8942d7f5fb496df46bbcad4a7103c46` | S16 x1 |
| data/r2/logs/U_in-200.log | `57020d3a95fae05cd20b48d23d71df8b8d937d6732b8319b9b2bfa0ee3e539f3` | `9b09b0eb1efd0d3c97fb9830f4d71f477ccd02bb8cc34da495887e82488ea6e2` | S16 x1 |
| data/r2/logs/U_lo-u.log | `4a8e7cff4b56d27e5ccd9a33eee0d0488c74c46da8bba87df21372ce082ea023` | `b6535be1f09f00aa7895ec85bfa4eef21d7539563f4f4bbf40755209d94c17c0` | S16 x1 |
| data/r2/logs/U_u150.log | `fdb661b2b8368762885851c1ad35f83be5bcaf8b24b7bafab30eca56aaff9da4` | `d33690fae6787abfe8f61a4e51e7bf922718a328ab43220b0046b3cc344620ff` | S16 x1 |
| data/r2/logs/U_u205.log | `af52013d8173586ffad375c6a694626864e362b57bd5c0bc60681862e6165e5f` | `6b1053e7fda73410d1d161826c90c8eb05aa14977adce46aed12845b7623fe31` | S16 x1 |
| code/r2/RUN.md | `ae0fa300c1085a0313951ca67618d6f9a9b77323f5b30a7a482fd2f2e0ab4015` | `f84084554fd02e6fcee51542a076b04ed4d42d9ce2a3a3ff4f9657559420626a` | S2 x1, S11 x2 |

## B. Instrument changes between runs (lab history)

- `code/r1/PATCHES-build2.md`: the referee-3 fixes that the sealed amendment AMENDMENT-R1-1 (6ad54f5713) applied to
  the first R1 instruments (σ0 = 9/5 exactly; exact final Riccati step; no float() on bounds; asserted margins;
  exterior margin minus ε; tube pinned by sha256). `code/r1/CALIBRATION.md`: the controls re-run with them.
- `code/r2/PATCHES-build3.md`: from R1 to R2 (four latent fixes found by the engine audit, the I_in clamp asked by
  referee-5, and the parameterisation in σ0 = p/q with an adaptive Cauchy disc and a separation record).
  `code/r2/CALIBRATION.md`: the R2 controls and the 9/5 regression, which reproduces R1 leaf for leaf.
  `code/r2/RUN.md`: the R2 hashes and commands (lab folders replaced, part A).
- These two notes name lab folders only in relative form (for example `core/seats/audit-1/`), which are not shipped.

## C. Repository tools (new for this release)

- `tools/check_numbers.py`: checks every row of NUMBERS.md against the file it names.
- `tools/make_scorecard.py`: builds scorecard.svg and SCORECARD.md, after checking the R1 verdict files.
- `figures/make_figures.py`: the two float figures, from `data/band-map/`.
- `tools/make_manifest.py` and `tools/canon.py`: copied from our previous release, unchanged.

## D. Notes on shipped documents (not edits)

- `proof/PROOF-R1-v2.md` is the 9/5 proof document and is shipped as the referees read it. Line 211 (Lemma 3.1, step 3)
  reads "F r0^2/6 < 2.5e-10". Read it as "< 2.5e-10 at 9/5 (<= 2.86e-10 at every R2 point)" (the R2 referee's
  recomputation). The step needs only < 1/100, which holds at every point, and the margins are asserted in code at
  every run. PAPER.md, Section 7.4, states how the proof transfers.
- `code/r2/verdict.py` (sealed instrument, not changed): `point_unstable` does not compare the sector of the certified
  eigenvalue with the sealed sector (`controls_r2` does). See PAPER.md, Section 9.
- `checks/check_frob_slack_r2.py` is the R2 referee's script, shipped with one line changed: its absolute release
  folder became `'.'` (run from the repository root). Its log `checks/check_frob_slack_r2.log` is a fresh run from the
  repository root; it is line-for-line identical to the referee's own output (memory-cap line aside).

## E. Clean-room findings applied (2026-11-19)
- tools/canon.py: `tube_source` (free-text build note, e.g. "built in this run (N s)") added to VOLATILE_KEYS. With it, every
  clean-room re-run (R1 target-B, target-K2; R2 B:lo-s, U:hi-u, K2:hi-s) is IDENTICAL-CANONICAL to the shipped data.
- reproduce.md: the expected-difference note now covers every job type; one SEALED-<tag>.ok per tag; verdict_blind prints scores only.
