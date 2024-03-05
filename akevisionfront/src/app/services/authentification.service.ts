import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {BehaviorSubject, Observable} from 'rxjs';
import {map} from 'rxjs/operators';
import {environment} from '../../environments/environment';
import {UserAuth} from '../model/userAuth';

const ANONYMOUS_USER = {
      user: {
        id: 0,
        username: 'Anonymous',
        password: '',
        firstName: '',
        lastName: '',
        groups: [],
      },
      token: '',
      deleting : false,

    } as UserAuth;


@Injectable({providedIn: 'root'})
export class AuthentificationService {

  static URL_BASE: string = environment.baseUrl + '/auth/';

  private currentUserSubject: BehaviorSubject<UserAuth>;

  constructor(private http: HttpClient) {
    const localUser = localStorage.getItem('currentUser')
    if (localUser) {
      // retrieve store user details and jwt token in local storage after page refreshes
      this.currentUserSubject = new BehaviorSubject<UserAuth>(UserAuth.parseJSON(localUser));
    } else {
      // set a anonymous user
      this.currentUserSubject = new BehaviorSubject<UserAuth>(UserAuth.fromJSON(ANONYMOUS_USER));
    }
  }

  public get currentUserValue(): UserAuth {
    return this.currentUserSubject.value;
  }

  public get currentUserObservable(): Observable<UserAuth> {
    return this.currentUserSubject.asObservable();
  }

  public login(username, password): Observable<any> {
    return this.http.post<any>(AuthentificationService.URL_BASE, {username, password})
      .pipe(map(user => {
        // store user details and jwt token in local storage to keep user logged in between page refreshes
        localStorage.setItem('currentUser', UserAuth.toJSON(user));
        this.currentUserSubject.next(UserAuth.fromJSON(user));
        return user;
      }));
  }

  public logout(): Observable<any> {
    // set that the current user wil be removed
    this.currentUserSubject.value.setDeleting(true);
    return this.http.delete(AuthentificationService.URL_BASE);
  }

  public removeCurrentUser() {
    // remove user from local storage after the send of a current user
    localStorage.removeItem('currentUser');
    this.currentUserSubject.next(UserAuth.fromJSON(ANONYMOUS_USER));
  }
}
