import {async, TestBed} from '@angular/core/testing';
import {AuthentificationService} from './authentification.service';
import {HttpClientTestingModule, HttpTestingController} from '@angular/common/http/testing';
import {User} from '../model/user';
import {UserAuth} from "../model/userAuth";

describe('AuthentificationService', () => {
  let httpMock: HttpTestingController;
  let service: AuthentificationService;

  const userAuthJson =
    {
      user: {
        id: 1,
        username: 'akema',
        password: 'password',
        firstName: 'first_akema',
        lastName: 'last_akema',
        groups: [1],
      },
      token: 'azerty',
    };

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

  const userAuth: UserAuth = UserAuth.fromJSON(userAuthJson);

  beforeEach(async(() => {

    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [AuthentificationService],
    });
    httpMock = TestBed.get(HttpTestingController);


  }));

  afterEach(async(() => {
    httpMock.verify();
  }));

  it('Test contructor with currentUser not null', () => {
    localStorage.setItem('currentUser', JSON.stringify(userAuth));
    service = TestBed.get(AuthentificationService);
    expect(UserAuth.fromJSON(service.currentUserValue)).toEqual(userAuth);
    expect(localStorage.getItem('currentUser')).toEqual(JSON.stringify(userAuth));
  });

  it('Test contructor with currentUser null', () => {
    localStorage.removeItem('currentUser');
    service = TestBed.get(AuthentificationService);
    expect(service.currentUserValue).toEqual(UserAuth.fromJSON(ANONYMOUS_USER));
    expect(localStorage.getItem('currentUser')).toBeNull();
  });


  it('Test logout', () => {
    localStorage.setItem('currentUser', JSON.stringify(userAuth));
    expect(localStorage.getItem('currentUser')).toEqual(JSON.stringify(userAuth));
    service = TestBed.get(AuthentificationService);

    service.logout().subscribe(logout => {
      expect(logout).toBeNull();
    });
    const http = httpMock.expectOne(`${AuthentificationService.URL_BASE}`);
    expect(http.request.method).toBe('DELETE');
    http.flush(null);
    expect(localStorage.getItem('currentUser')).toEqual(UserAuth.toJSON(userAuth));
    userAuth.setDeleting(true);
    expect(UserAuth.fromJSON(service.currentUserValue)).toEqual(userAuth);
  });

  it('Test login', () => {
    localStorage.removeItem('currentUser');
    service = TestBed.get(AuthentificationService);
    expect(service.currentUserValue).toEqual(UserAuth.fromJSON(ANONYMOUS_USER));
    expect(localStorage.getItem('currentUser')).toBeNull();

    service.login(userAuth.user.username, userAuth.user.password).subscribe(loginUser => {
      expect(loginUser).toBe(userAuth);
    });
    const http = httpMock.expectOne(`${AuthentificationService.URL_BASE}`);
    expect(http.request.method).toBe('POST');
    http.flush(userAuth);
    expect(service.currentUserValue).toEqual(userAuth);
    expect(localStorage.getItem('currentUser')).toEqual(UserAuth.toJSON(userAuth));
  });

  it('Test removeCurrentUser', () => {
    localStorage.setItem('currentUser', JSON.stringify(userAuth));
    expect(localStorage.getItem('currentUser')).toEqual(JSON.stringify(userAuth));
    service = TestBed.get(AuthentificationService);

    service.removeCurrentUser();

    expect(service.currentUserValue).toEqual(UserAuth.fromJSON(ANONYMOUS_USER));
    expect(localStorage.getItem('currentUser')).toBeNull();
  });

});
