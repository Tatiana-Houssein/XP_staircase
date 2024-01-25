import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ImageService {
  constructor(private http: HttpClient) {}

  getImage(id: number): Observable<string> {
    const url = `assets/tokens_${id}.png`;

    // Set headers to prevent caching
    const headers = new HttpHeaders().set('Cache-Control', 'no-store');

    return this.http.get(url, { responseType: 'text', headers });
  }
}
