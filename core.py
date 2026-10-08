import datetime, hashlib, hmac, math, secrets
DIVS=['Pengurus Inti','Ketahanan','Kewirausahaan','Seni Budaya','Kesehatan','Keolahragaan','Sosial','Humas','Keagamaan']
ROLES=['pembina','ketua','wakil','sekretaris','bendahara','ketua_divisi','anggota']
def hashpw(password):
    salt=secrets.token_hex(16)
    return 'pbkdf2$240000$'+salt+'$'+hashlib.pbkdf2_hmac('sha256',password.encode(),salt.encode(),240000).hex()
def checkpw(stored,password):
    try:
        scheme,iterations,salt,digest=stored.split('$')
        if scheme!='pbkdf2' or not 100000<=int(iterations)<=2000000:return False
        return hmac.compare_digest(digest,hashlib.pbkdf2_hmac('sha256',password.encode(),salt.encode(),int(iterations)).hex())
    except (ValueError,TypeError,AttributeError):return False
def admin(user):return user['role'] in ('pembina','ketua')
def can_read(user,kind,kinds):
    if kind not in kinds:return False
    div=kinds[kind].get('division')
    if div:return user['role'] in ('pembina','ketua','wakil') or user['division']==div
    if kind=='letters':return user['role'] in ('pembina','ketua','wakil','sekretaris')
    return True
def can_write(user,kind,div,kinds):
    if kind not in kinds:return False
    if admin(user):return True
    role=user['role'];own=kinds[kind].get('division')
    if own:return role in ('ketua_divisi','anggota') and user['division']==own
    if kind=='finance':return role=='bendahara'
    if kind=='letters':return role=='sekretaris'
    if kind=='announcements':return role in ('wakil','sekretaris')
    if kind=='events':return role in ('wakil','sekretaris') or (role=='ketua_divisi' and div==user['division'])
    if kind=='tasks':return role=='wakil' or (role=='ketua_divisi' and div==user['division'])
    return False
def clean(kind,data,kinds):
    if not isinstance(data,dict):raise ValueError('Data harus berupa objek.')
    result={}
    for field in kinds[kind]['fields']:
        name=field['name'];value=data.get(name);t=field['type']
        if value is None or (isinstance(value,str) and not value.strip()):
            if field['required']:raise ValueError(field['label']+' wajib diisi.')
            result[name]='';continue
        if t=='number':
            if isinstance(value,bool):raise ValueError('Angka tidak valid.')
            n=float(value)
            if not math.isfinite(n) or n<0 or n>1e12 or (kind=='finance' and n<=0):raise ValueError('Nominal/jumlah tidak valid.')
            result[name]=int(n) if n.is_integer() else n
        else:
            s=str(value).strip()
            if len(s)>5000:raise ValueError('Isi terlalu panjang.')
            if t=='date':s=datetime.date.fromisoformat(s).isoformat()
            if t=='time':datetime.time.fromisoformat(s)
            if t=='select' and s not in field['choices']:raise ValueError(field['label']+' tidak dikenal.')
            result[name]=s
    return result
