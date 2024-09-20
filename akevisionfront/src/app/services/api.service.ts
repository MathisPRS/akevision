import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { Observable, map } from 'rxjs';


@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = environment.baseUrl;

  constructor(private http: HttpClient) { }

  get(endpoint: string, options) {
    return this.http.get(`${this.apiUrl}${endpoint}`, options);
  }

  post(endpoint: string, data: any) {
    return this.http.post(`${this.apiUrl}${endpoint}`, data);
  }

  put(endpoint: string, data: any) {
    return this.http.put(`${this.apiUrl}${endpoint}`, data);
  }

  delete(endpoint: string) {
    return this.http.delete(`${this.apiUrl}${endpoint}`);
  }

  getAllGroupesWebsite(): Observable<any> {
    return this.get('/groupes-websites/','');
  }
  getAllCompagnies(): Observable<any> {
    return this.get('/compagnies/','').pipe(
      map(response => response['results'])
    );
  }
  getAllWebsite(): Observable<any> {
    return this.get('/websites/','').pipe(
      map(response => response['results'])
    );
  }
  
  buildAgent(client: any): Observable<any> {
    return this.post('/agents/', {
      os: client.os,
      compagnie_id: client.compagnie_id,
    },);
  }

  createCompagnie(name: string): Observable<any> {
    const body = { name };
    return this.post('/compagnies/', body);
  }


}
