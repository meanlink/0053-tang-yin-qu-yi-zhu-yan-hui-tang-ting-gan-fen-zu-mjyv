INSERT INTO seats VALUES
 ('A1','南棚小堂','front',1,true),('A2','南棚小堂','front',2,true),
 ('B1','南棚小堂','mid',1,true),('B2','南棚小堂','mid',2,true),
 ('C1','南棚小堂','rear',1,false),('C2','南棚小堂','rear',2,true),
 ('D1','西厢分场','mid',1,true)
 ON CONFLICT DO NOTHING;
INSERT INTO listening_slips VALUES
 ('A1','spoken',90,260,64,'说段-A1.wav'),('A1','sung',86,280,68,'唱段-A1.wav'),
 ('A2','spoken',87,271,63,'说段-A2.wav'),('A2','sung',88,279,66,'唱段-A2.wav'),
 ('B1','spoken',64,660,60,'说段-B1.wav'),('B1','sung',61,694,62,'唱段-B1.wav'),
 ('B2','spoken',66,688,61,'说段-B2.wav'),('B2','sung',60,671,61,'唱段-B2.wav'),
 ('C1','spoken',49,905,53,'说段-C1.wav'),('C1','sung',49,941,55,'唱段-C1.wav'),
 ('C2','spoken',49,903,54,'说段-C2.wav'),('C2','sung',47,935,56,'唱段-C2.wav'),
 ('D1','spoken',80,290,65,'说段-D1.wav') ON CONFLICT DO NOTHING;
INSERT INTO listening_layouts VALUES ('S1','南棚小堂','固定侧墙反射板',0,3),('S2','南棚小堂','中区软面吸声板',3,3),
 ('S3','西厢分场','分场铺垫',3,4) ON CONFLICT DO NOTHING;
INSERT INTO residency_slots VALUES ('N-28','南棚小堂','杜箐','2026-11-28'),('N-29','南棚小堂','郭杨','2026-11-29'),
 ('W-29','西厢分场','陈意','2026-11-29') ON CONFLICT DO NOTHING;
