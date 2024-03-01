import {async, TestBed} from '@angular/core/testing';

import {RestService} from './rest.service';
import {HttpClientTestingModule, HttpTestingController} from '@angular/common/http/testing'
import {environment} from '../../environments/environment';
import {User} from "../model/user";

describe('RestService', () => {
  let httpMock: HttpTestingController;
  let service: RestService;

  const endPoint = '/users/';
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
      providers: [RestService],
    });
    httpMock = TestBed.get(HttpTestingController);
    service = TestBed.get(RestService);

  }));

  afterEach(async(() => {
    httpMock.verify();
  }));

  // test list method
  it('Test list method no param - should retrieve User[]', () => {
    service.list(endPoint).subscribe(users => {
      expect(users.length).toBe(2);
      expect(users).toBe(dummyUsers);
    });
    const http = httpMock.expectOne(`${environment.baseUrl + endPoint}`);
    expect(http.request.method).toBe('GET');
    http.flush(dummyUsers);
  });

  it('Test list method with param - should retrieve User[]', () => {
    const param = {
      param1: 1,
      param2: 'param2',
    };
    service.list(endPoint, param).subscribe(users => {
      expect(users.length).toBe(2);
      expect(users).toBe(dummyUsers);
    });
    const http = httpMock.expectOne(`${environment.baseUrl + endPoint}?param1=1&param2=param2`);
    expect(http.request.method).toBe('GET');
    http.flush(dummyUsers);
  });

  // test page method
  it('Test page method no param - should retrieve User[]', () => {
    service.page(endPoint, 5).subscribe(users => {
      expect(users.length).toBe(2);
      expect(users).toBe(dummyUsers);
    });
    const http = httpMock.expectOne(`${environment.baseUrl + endPoint}?page=5`);
    expect(http.request.method).toBe('GET');
    http.flush(dummyUsers);
  });

  it('Test list method with param - should retrieve User[]', () => {
    const param = {
      param1: 1,
      param2: 'param2',
    };
    service.page(endPoint, 5, param).subscribe(users => {
      expect(users.length).toBe(2);
      expect(users).toBe(dummyUsers);
    });
    const http = httpMock.expectOne(`${environment.baseUrl + endPoint}?page=5&param1=1&param2=param2`);
    expect(http.request.method).toBe('GET');
    http.flush(dummyUsers);
  });

  // test retrieve method
  it('Test retrieve method - should retrieve User', () => {
    service.retrieve(endPoint, 5).subscribe(user => {
      expect(user).toBe(dummyUsers[0]);
    });
    const http = httpMock.expectOne(`${environment.baseUrl + endPoint}5/`);
    expect(http.request.method).toBe('GET');
    http.flush(dummyUsers[0]);
  });

  // test create method
  it('Test create method - should create User', () => {
    const body: any =
      {
        username: 'akema',
        password: 'password',
        firstName: 'first_akema',
        lastName: 'last_akema',
        token: 'azerty',
      }

    service.create(endPoint, body).subscribe(user => {
      expect(user).toBe(dummyUsers[0]);
    });
    const http = httpMock.expectOne(`${environment.baseUrl + endPoint}`);
    expect(http.request.method).toBe('POST');
    http.flush(dummyUsers[0]);
  });

  // test delete method
  it('Test delete method no pk - should retrieve User', () => {
    let pk: any;
    service.delete(endPoint, pk).subscribe(user => {
      expect(user).toBeNull();
    });
    const http = httpMock.expectOne(`${environment.baseUrl + endPoint}`);
    expect(http.request.method).toBe('DELETE');
    http.flush(null);
  });

  it('Test delete method with pk param', () => {
    const pk: any = 5;
    service.delete(endPoint, pk).subscribe(user => {
      expect(user).toBeNull();
    });
    const http = httpMock.expectOne(`${environment.baseUrl + endPoint}5/`);
    expect(http.request.method).toBe('DELETE');
    http.flush(null);
  });

  // test update method
  it('Test update method - should retrieve User', () => {
    const pk: any = 5;
    const body: any =
      {
        username: 'akemaold',
      }
    service.partialUpdate(endPoint, pk, body).subscribe(user => {
      expect(user).toBe(dummyUsers[0]);
    });
    const http = httpMock.expectOne(`${environment.baseUrl + endPoint}5/`);
    expect(http.request.method).toBe('PATCH');
    http.flush(dummyUsers[0]);
  });

});
