import {Injectable} from '@angular/core';
import {Router, NavigationStart} from '@angular/router';
import {BehaviorSubject, Observable} from 'rxjs';
import {Alert} from '../model/alert';

@Injectable({providedIn: 'root'})
export class AlertService {

  private subject: BehaviorSubject<Alert> = new BehaviorSubject<Alert>(new Alert('none', ''));
  private keepAfterRouteChange = false;

  constructor(private router: Router) {
    // clear alert messages on route change unless 'keepAfterRouteChange' flag is true
    this.router.events.subscribe(event => {
        if (event instanceof NavigationStart) {
          if (this.keepAfterRouteChange) {
            // only keep for a single route change
            console.log('router events alert keepAfterRouteChange');
            this.keepAfterRouteChange = false;
          } else {
            // clear alert message
            this.clear();
          }
        }
      }, () => console.log('router events alert error'),
      () => console.log('router events alert complete'));
  }

  public getAlert(): Observable<any> {
    return this.subject.asObservable();
  }

  public get currentAlertValue(): Alert {
    return this.subject.value;
  }

  public success(message: string, keepAfterRouteChange = false) {
    this.keepAfterRouteChange = keepAfterRouteChange;
    this.subject.next(new Alert('success', message));
  }

  public error(message: string, keepAfterRouteChange = false) {
    console.log('AlertService failed');
    this.keepAfterRouteChange = keepAfterRouteChange;
    this.subject.next(new Alert('error', message));
  }
  public warning(message: string, keepAfterRouteChange = false) {
    this.keepAfterRouteChange = keepAfterRouteChange;
    this.subject.next(new Alert('warning', message));
  }

  public clear() {
    // clear by calling subject.next() without parameters
    if (this.currentAlertValue.notClear()) {
      this.subject.next(new Alert('none', ''));
    }
  }
}
