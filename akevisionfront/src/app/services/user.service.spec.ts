import {async, TestBed} from '@angular/core/testing';

import {UserService} from './user.service';
import {HttpClientTestingModule, HttpTestingController} from '@angular/common/http/testing';
import {User} from '../model/user';
import {environment} from '../../environments/environment';
import {RestService} from './rest.service';

describe('UserService', () => {
  let httpMock: HttpTestingController;
  let service: UserService;

  let userJson =
    {
      id: 1,
      username: 'akema',
      password: 'password',
      firstName: 'first_akema',
      lastName: 'last_akema',
      groups: [1],
    };
  const user1 = User.fromJSON(userJson);
  userJson =
    {
      id: 1,
      username: 'test',
      password: 'testpassword',
      firstName: 'first_test',
      lastName: 'last_test',
      groups: [1, 2],
    };
  const user2 = User.fromJSON(userJson);

  const dummyUsers: User[] = [user1, user2];


  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [UserService, RestService],
    });
    httpMock = TestBed.get(HttpTestingController);
    service = TestBed.get(UserService);

  }));

  afterEach(async(() => {
    httpMock.verify();
  }));

  // test list method
  it('Test getAll method - should retrieve User[]', () => {
    service.getAll().subscribe(users => {
      expect(users.length).toBe(2);
      expect(users).toBe(dummyUsers);
    });
    const http = httpMock.expectOne(`${environment.baseUrl + UserService.USERS_URL_BASE}`);
    expect(http.request.method).toBe('GET');
    http.flush(dummyUsers);
  });

  it('Test delete method with pk param', () => {
    const id: any = 5;
    service.delete(id).subscribe(user => {
      expect(user).toBeNull();
    });
    const http = httpMock.expectOne(`${environment.baseUrl + UserService.USERS_URL_BASE}5/`);
    expect(http.request.method).toBe('DELETE');
    http.flush(null);
  });

  // test create method
  it('Test create method - should create User', () => {
    const userJson =
      {
        id: 1,
        username: 'akema',
        password: 'password',
        firstName: 'first_akema',
        lastName: 'last_akema',
        groups: [1],
      };
    const newUser = User.fromJSON(userJson);

    service.register(newUser).subscribe(user => {
      expect(user).toBe(dummyUsers[0]);
    });
    const http = httpMock.expectOne(`${environment.baseUrl + UserService.USERS_URL_BASE}`);
    expect(http.request.method).toBe('POST');
    http.flush(dummyUsers[0]);
  });
});
