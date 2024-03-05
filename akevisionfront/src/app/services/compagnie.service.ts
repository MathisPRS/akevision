// compagnie.service.ts

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ApiService  } from './api.service';

@Injectable({
  providedIn: 'root'
})
export class CompagnieService {

  constructor(private http: HttpClient, private apiService: ApiService  ) { }

  createCompagnie(compagnie: any): Observable<any> {
    return this.apiService.post('/compagnies/', compagnie)
  }
}
