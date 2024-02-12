import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-info-second-task',
  templateUrl: './info-second-task.component.html',
  styleUrls: ['./info-second-task.component.scss']
})
export class InfoSecondTaskComponent {
  constructor(private router: Router) {}


  sendToExperiment(): void {
    this.router.navigate(['/experiment']);
  }
}
