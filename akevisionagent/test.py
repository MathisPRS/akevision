import psutil
import subprocess
import datetime

def get_disk_info():
    disk_info = []
    partitions = psutil.disk_partitions()
    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_info.append({
                "device": partition.device,
                "mountpoint": partition.mountpoint,
                "fstype": partition.fstype,
                "total": usage.total,
                "used": usage.used,
                "free": usage.free,
                "percent": usage.percent
            })
        except PermissionError as e:
            print(f"PermissionError: {e} for partition {partition.device}")
        except Exception as e:
            print(f"Error: {e} for partition {partition.device}")
    return disk_info

def check_for_updates():
    try:
        result = subprocess.run(['wuauclt.exe', '/detectnow'], capture_output=True, text=True)
        if result.returncode == 0:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error checking for updates: {e}")
        return False

def get_critical_events():
    try:
        # Calculer la date de début pour les 7 derniers jours
        start_date = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime('%Y-%m-%dT%H:%M:%S')

        # Utiliser wevtutil pour filtrer les événements critiques (niveau de gravité 1) des 7 derniers jours
        result = subprocess.run(
            ['wevtutil', 'qe', 'System', '/c:10', '/f:text', '/q:*[System[(Level=1) and TimeCreated[@SystemTime>=\'{}\']]]'.format(start_date)],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            return result.stdout
        else:
            return None
    except Exception as e:
        print(f"Error getting critical events: {e}")
        return None

def main():
    # Vérifier l'état des disques
    disk_info = get_disk_info()
    print("Disk Information:")
    for disk in disk_info:
        print(disk)

    # Vérifier s'il y a des mises à jour sur le poste
    updates_available = check_for_updates()
    print("\nUpdates Available:", updates_available)

    # Récupérer des événements critiques
    critical_events = get_critical_events()
    print("\nCritical Events:")
    if critical_events:
        print(critical_events)
    else:
        print("No critical events found or error occurred.")

if __name__ == "__main__":
    main()
