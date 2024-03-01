import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {User} from '../model/user';
import {map} from 'rxjs/operators';
import {environment} from '../../environments/environment';
import {RestService} from './rest.service';
import {Group} from '../model/group';

@Injectable({
  providedIn: 'root'
})

export class UserService {
  static USERS_URL_BASE = '/users/';
  static GROUPS_URL_BASE = '/groups/';

  constructor(private http: RestService) {
  }

  public groupList(): Observable<Group[]> {
    return this.http.list<Group[]>(UserService.GROUPS_URL_BASE);
  }

  public getAll(): Observable<User[]> {
    return this.http.list<User[]>(UserService.USERS_URL_BASE);
  }

  public register(user: User): Observable<User> {
    return this.http.create<User>(UserService.USERS_URL_BASE, user);
  }

  public delete(id: number): Observable<any> {
    return this.http.delete(UserService.USERS_URL_BASE, id);
  }
}
