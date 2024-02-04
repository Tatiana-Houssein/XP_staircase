import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { Store } from '@ngrx/store';
import { loadExperimentComponent } from 'src/app/@store/actions';
import { AppState } from 'src/app/@store/app.state';

@Component({
  selector: 'app-user-info',
  templateUrl: './user-info.component.html',
  styleUrls: ['./user-info.component.scss']
})
export class UserInfoComponent {
  constructor(private router: Router, private store: Store<AppState>) {}


  ngOnInit(): void {
    this.store.dispatch(loadExperimentComponent());
  }

  sendToExperiment(): void {
    this.router.navigate(['/experiment']);
  }

}
