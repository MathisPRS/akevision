import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ApiService } from './api.service';

@Injectable({
  providedIn: 'root'
})
export class CompagnieService {

  constructor(private http: HttpClient, private apiService: ApiService) { }

  createCompagnie(name: string): Observable<any> {
    const body = { name }; // encapsuler les données de la forme dans un objet JSON avec la propriété name
    return this.apiService.post('/compagnies/', body);
  }
}
