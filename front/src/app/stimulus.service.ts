import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Stimulus } from './stimulus.model';
@Injectable({
  providedIn: 'root'
})
export class StimulusService {

  url: string = 'http://localhost:5000'

  constructor(private httpClient: HttpClient ) {}

  getTestToken(): Observable<any> {
    const token = this.httpClient.get<Stimulus>(`${this.url}/first-stimulus`);
    return token;
  }

}
