import {ChangeDetectorRef, Component, OnDestroy, OnInit} from '@angular/core';
import {Router} from '@angular/router';
import {AuthentificationService} from './services/authentification.service';
import {UserAuth} from './model/userAuth';
import {Subscription} from 'rxjs';
import {environment} from '../environments/environment';
import {MediaMatcher} from "@angular/cdk/layout";
import {UserService} from "./services/user.service";


// import './_content/app.less';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit, OnDestroy {

  private subscription: Subscription;
  currentUser: UserAuth;
  mdq: MediaQueryList;
  mediaQueryListener: () => void;
  groupeQualiteFlag: boolean;
  groupeMonnayeurFlag: boolean;
  prodFlag = environment.production;

  constructor(    private router: Router,
    private authenticationService: AuthentificationService,
    private changeDetectorRef: ChangeDetectorRef,
    private media: MediaMatcher, private userService: UserService
  )  {
    this.mdq = media.matchMedia('(max-width: 769px)');
    this.mediaQueryListener = () => {
      changeDetectorRef.detectChanges(); };
    this.mdq.addListener(this.mediaQueryListener);

  }

  ngOnInit() {
    console.log(this.currentUser)
    this.subscription = this.authenticationService.currentUserObservable.subscribe(
      x => {
        console.log('APP Login OK')
        this.currentUser = UserAuth.fromJSON(x);
        this.groupeQualiteFlag = this.currentUser.isUserAuthInGroup(1);
        this.groupeMonnayeurFlag = this.currentUser.isUserAuthInGroup(2);
      },
      () => console.log('APP Login error'),
      () => console.log('APP Login complete')
    )
    ;
  }

  openCloseNav() {
    const navMaxLength = '222px';
    const navMinLength = '50px';
    if (!this.mdq.matches) {
      if (document.getElementById('mySidenav').style.width === navMaxLength
        && document.getElementById('container').style.marginLeft === navMaxLength) {
        document.getElementById('mySidenav').style.width = navMinLength;
        document.getElementById('container').style.marginLeft = '0';
      } else {
        document.getElementById('mySidenav').style.width = navMaxLength;
        document.getElementById('container').style.marginLeft = navMaxLength;
      }}
    }

  logout() {
    this.authenticationService.logout().subscribe(
      () => {
        console.log('APP Logout OK');
        this.router.navigate(['/login']);
      },
      () => console.log('APP Logout error'),
      () => console.log('APP Logout complete')
    )
    ;
  }

  ngOnDestroy() {
    console.log('APP Login ngOnDestroy')
    this.subscription.unsubscribe();
  }
}
