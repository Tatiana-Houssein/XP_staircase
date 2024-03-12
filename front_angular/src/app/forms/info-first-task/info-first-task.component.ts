import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-info-first-task',
  templateUrl: './info-first-task.component.html',
  styleUrls: ['./info-first-task.component.scss'],
})
export class InfoFirstTaskComponent {
  constructor(private router: Router) {}

  sendToExperiment(): void {
    this.router.navigate(['/experiment']);
  }
}
