import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ImageService {
  constructor(private http: HttpClient) {}

  private imageBaseUrl = 'assets/tokens/'
  getImage(id: number): Observable<string> {
    const url = `assets/tokens/tokens_${id}.png`;

    // Set headers to prevent caching
    const headers = new HttpHeaders().set('Cache-Control', 'no-store');

    return this.http.get(url, { responseType: 'text', headers });
  }

  getImageUrlAsset(id: number): string {
    return `assets/tokens/tokens_${id}.png`;
  }

  getImageUrl(imageId: number): string {
    // Assuming image files are named like "image_1.jpg", "image_2.jpg", etc.
    return `${this.imageBaseUrl}token_${imageId}.png`;
  }
}
