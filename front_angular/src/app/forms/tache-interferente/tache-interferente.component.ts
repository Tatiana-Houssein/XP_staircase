// second-page.component.ts

import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-tache-interferente',
  templateUrl: './tache-interferente.component.html',
  styleUrls: ['./tache-interferente.component.scss']
})
export class TacheInterferenteComponent {
  constructor(private router: Router) {}

  goBack(): void {
    this.router.navigate(['/experiment']);
  }
}
