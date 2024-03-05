import {Component, OnInit, OnDestroy} from '@angular/core';
import {Subscription} from 'rxjs';
import {AlertService} from '../../services/alert.service';


@Component({
  selector: 'app-alert',
  templateUrl: './alert.component.html',
  styleUrls: ['./alert.component.scss']
})
export class AlertComponent implements OnInit, OnDestroy {
  private subscription: Subscription = null;
  alert: any;

  constructor(private alertService: AlertService) {
  }

  ngOnInit() {
    this.subscription = this.alertService.getAlert()
      .subscribe(alert => {
          switch (alert && alert.type) {
            case 'success':
              alert.cssClass = 'alert alert-success';
              break;
            case 'error':
              alert.cssClass = 'alert alert-danger';
              break;
              case 'warning':
              alert.cssClass = 'alert alert-warning';
              break;
          }
          this.alert = alert;
        },
        () => console.log('alert error'),
        () => console.log('alert complete'));
  }

  ngOnDestroy() {
    // unsubscribe to ensure no memory leaks
    if (this.subscription){
      this.subscription.unsubscribe();
    }
  }
}
