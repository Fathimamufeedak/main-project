import urllib.request

urls = [
    'http://127.0.0.1:8000/',
    'http://127.0.0.1:8000/register/',
    'http://127.0.0.1:8000/login/',
    'http://127.0.0.1:8000/plants/',
    'http://127.0.0.1:8000/consultations/upload/',
    'http://127.0.0.1:8000/consultations/my/',
    'http://127.0.0.1:8000/admin/',
    'http://127.0.0.1:8000/adminpanel/doctor-requests/',
    'http://127.0.0.1:8000/doctors/register/',
]

def fetch(url):
    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            data = r.read(2048)
            print(f"{url} -> {r.status} {r.reason} | {len(data)} bytes | preview: {data[:200]!r}")
    except Exception as e:
        print(f"{url} -> ERROR: {e}")


if __name__ == '__main__':
    for u in urls:
        fetch(u)
