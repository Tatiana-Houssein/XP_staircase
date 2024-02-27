import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Stimulus } from '../stimulus.model';
@Injectable({
  providedIn: 'root',
})
export class StimulusService {
  url: string = 'http://localhost:5000';

  constructor(private httpClient: HttpClient) {}

  getFirstStimulus(): Observable<any> {
    const token = this.httpClient.get<Stimulus>(`${this.url}/first-stimulus`);
    return token;
  }

  sendSubjectAnswer(dejaVu: boolean): Observable<any> {
    const stimulus = this.httpClient.post<boolean>(
      `${this.url}/next-stimulus`,
      dejaVu
    );
    return stimulus;
  }
}
