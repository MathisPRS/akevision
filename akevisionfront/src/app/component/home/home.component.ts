import {Component, OnInit} from '@angular/core';
import {UserService} from '../../services/user.service';
import {AlertService} from '../../services/alert.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  users = [];

  constructor(
    private userService: UserService,
    private alertService: AlertService
  ) {
  }

  ngOnInit() {
    //this.loadAllUsers();
  }

  deleteUser(id: number) {
    this.userService.delete(id)
      .subscribe(() => {
          console.log('deleteUser OK');
          this.loadAllUsers();
        },
        error => {
          this.alertService.error(error.error.message || error.statusText);
          console.log('deleteUser error');
        },
        () => console.log('deleteUser complete'));
  }

  private loadAllUsers() {
    // reset alerts on submit
    this.alertService.clear();

    this.userService.getAll()
      .subscribe(users => {
          console.log('loadAllUsers OK');
          this.users = users;
        }, error => {
          this.alertService.error(error.error.message || error.statusText);
          console.log('loadAllUsers error');
        },
        () => console.log('loadAllUsers complete'));
  }
}
