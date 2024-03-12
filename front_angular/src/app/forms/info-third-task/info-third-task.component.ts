import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-info-third-task',
  templateUrl: './info-third-task.component.html',
  styleUrls: ['./info-third-task.component.scss'],
})
export class InfoThirdTaskComponent {
  constructor(private router: Router) {}

  sendToExperiment(): void {
    this.router.navigate(['/experiment']);
  }
}
