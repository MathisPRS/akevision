import {Component, OnInit} from '@angular/core';
import {Router} from '@angular/router';
import {UntypedFormBuilder, FormControl, UntypedFormGroup, Validators} from '@angular/forms';
import {first} from 'rxjs/operators';
import {AuthentificationService} from '../../services/authentification.service';
import {UserService} from '../../services/user.service';
import {AlertService} from '../../services/alert.service';
import {User} from '../../model/user';
import {Group} from '../../model/group';


@Component({
  // selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent implements OnInit {
  registerForm: UntypedFormGroup;
  loading = false;
  submitted = false;
  model: User = new User();
  groups: Group[];

  constructor(
    private formBuilder: UntypedFormBuilder,
    private router: Router,
    private authenticationService: AuthentificationService,
    private userService: UserService,
    private alertService: AlertService
  ) {
    // redirect to home if already logged in
    if (this.authenticationService.currentUserValue.token !== '') {
      this.router.navigate(['/']);
    }
  }

  ngOnInit() {
    this.groups = [];
    this.userService.groupList().subscribe(
      data => {
        console.log('user groupList OK');
        this.groups = data;
      },
      error => {
        this.alertService.error(error.error.message || error.statusText);
        console.log('user groupList error');
      },
      () => console.log('user groupList complete'));
    this.registerForm = this.formBuilder.group({
      firstName: [this.model.firstName, Validators.required],
      lastName: [this.model.lastName, Validators.required],
      username: [this.model.username, Validators.required],
      password: [this.model.password, [Validators.required, Validators.minLength(6)]],
      groupe: ['', Validators.required]
    });
  }

  // convenience getter for easy access to form fields
  get f() {
    return this.registerForm.controls;
  }

  onSubmit() {
    this.submitted = true;

    // reset alerts on submit
    this.alertService.clear();

    // stop here if form is invalid
    if (this.registerForm.invalid) {
      return;
    }

    this.loading = true;
    this.model.groups = [this.registerForm.value.groupe];
    // this.model.groups = [];
    this.userService.register(this.model)
      .pipe(first())
      .subscribe(
        data => {
          console.log('register OK');
          this.alertService.success('Registration successful', true);
          this.router.navigate(['/login']);
        },
        error => {
          this.alertService.error('Impossible d\'enregister le nouvel utilisateur');
          this.loading = false;
          console.log('register error:', error);
        },
        () => console.log('register complete'));
  }
}
