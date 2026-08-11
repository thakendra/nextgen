import os
import paramiko

old_files = [
    'arthashree-ventures.html', 'balkot-home.html', 'bhanu-panta-home.html',
    'bharatpur-residence.html', 'bhattrai-home.html', 'buddhanilkhantha-exterior.html',
    'chitwan-home.html', 'chunikhel-home.html', 'dang-home.html',
    'gautam-hotel.html', 'gumba-maharajgunj.html', 'jayant-ji-home.html',
    'jorpati-home.html', 'kl-tower-skincare.html', 'lemon-tree.html',
    'lilly-residence.html', 'lokhanthali-home.html', 'maya-cafe.html',
    'mulpani-gautam-hotel.html', 'munneys-salon.html', 'naran-lama-home.html',
    'navya-hotel.html', 'nayaparti-home.html', 'photobooth-civil-mall.html',
    'rajan-rai-home.html', 'ramkot-home.html', 'renu-gurung-home.html',
    'roshan-home.html', 'sankhu-exterior.html', 'sitapaila-banquet.html',
    'sitapaila-home.html', 'thakendra-khadka-house.html',
    'Thakendra khadka house.html', 'thulo-bharang-banquet.html', 'tokha-home.html',
    'bhanu panta exterior design nextgen interior .html'
]

# Delete locally
for f in old_files:
    local_path = os.path.join(r"D:\nextgen", f)
    if os.path.exists(local_path):
        os.remove(local_path)
        print(f"Deleted local: {f}")

# Delete from Hostinger
try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('srv1046530.hstgr.cloud', 22, 'root', 'UbSMVZUfEYRFHn5@M9y#', timeout=15)
    for f in old_files:
        ssh.exec_command(f'rm -f "/var/www/nextgen/{f}"')
    ssh.close()
    print("Deleted all old files from Hostinger /var/www/nextgen!")
except Exception as e:
    print("Hostinger cleanup note:", e)
