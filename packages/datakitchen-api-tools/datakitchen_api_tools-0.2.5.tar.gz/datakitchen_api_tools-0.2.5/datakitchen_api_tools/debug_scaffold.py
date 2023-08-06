from DKConnection import DKConnection

conn = DKConnection("cloud.datakitchen.io", "armand+hm@datakitchen.io", "%Gun8D9M")
results = conn.safeCreateOrder("hemonc_sftp_automation", 'hemonc_sftp_automation' ,'test-variation')
