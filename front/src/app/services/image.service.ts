import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class ImageService {
  private imageBaseUrl = 'assets/visages/';

  getImageUrl(imageId: number): string {
    return `${this.imageBaseUrl}visage-${imageId}.png`;
  }
}
