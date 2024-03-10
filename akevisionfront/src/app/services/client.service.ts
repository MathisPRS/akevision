import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ApiService } from './api.service';

@Injectable({
  providedIn: 'root'
})
export class ClientService {

  constructor(private http: HttpClient, private apiService: ApiService) { }

  createClient(client: any): Observable<any> {
    return this.apiService.post('/clients/', {
      name: client.name,
      os: client.os,
      compagnie_id: client.compagnie_id // modifié ici
    });
  }
}
