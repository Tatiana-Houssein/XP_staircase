import { Component } from '@angular/core';
import { Observable, map } from 'rxjs';
import {
  AppState,
  selectCurrentId,
  selectIsExperimentLaunched,
  selectNextId,
} from '../../@store/app.state';
import { increment } from '../../@store/actions';
import { Store } from '@ngrx/store';

@Component({
  selector: 'app-despair',
  templateUrl: './despair.component.html',
  styleUrls: ['./despair.component.scss'],
})
export class DespairComponent {
  currentId$: Observable<number>;
  nextId$: Observable<number>;
  isExperimentLaunched$: Observable<boolean>;

  constructor(private store: Store<AppState>) {
    this.currentId$ = store.select(selectCurrentId);
    this.nextId$ = store.select(selectNextId);
    this.isExperimentLaunched$ = this.store.select(selectIsExperimentLaunched);
  }
}
