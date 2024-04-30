import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Stimulus } from '../stimulus.model';


@Injectable({
  providedIn: 'root',
})
export class StimulusService {
  apiUrl: string = 'http://localhost:5000';

  constructor(private httpClient: HttpClient) {}

  getFirstStimulus(): Observable<any> {
    const token = this.httpClient.get<Stimulus>(
      `${this.apiUrl}/first-stimulus`
    );
    return token;
  }

  sendSubjectAnswer(chosenNumber: number): Observable<any> {
    const stimulus = this.httpClient.post<boolean>(
      `${this.apiUrl}/next-stimulus`,
      chosenNumber
    );
    return stimulus;
  }

  sendForm(formValue: any) {
    this.httpClient.post(`${this.apiUrl}/submit`, formValue).subscribe(
      (response) => {
        console.log('Form submitted successfully:', response);
        // Handle response if needed
      },
      (error) => {
        console.error('Error submitting form:', error);
        // Handle error if needed
      }
    );
  }

  requestTacheinterferente() {
    return this.httpClient.get<any>(`${this.apiUrl}/tache-interferente`);
  }
}
