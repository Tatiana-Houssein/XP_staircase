import { Injectable } from "@angular/core";
import { Actions, createEffect, ofType } from "@ngrx/effects";
import { loadExperimentComponent, receivedBackAnswer } from './actions';
import { responseUserToStimulus } from './actions';
import { filter, map, mergeMap, switchMap, tap, withLatestFrom } from "rxjs";
import { StimulusService } from "../services/stimulus.service";
import { AppState, selectIsExperimentLaunched } from "./app.state";
import { Store, select } from "@ngrx/store";

@Injectable()
export class AppEffects {

  loadComponent$ = createEffect(() =>
    this.actions$.pipe(
      ofType(loadExperimentComponent), // assuming you have an action for component load
      withLatestFrom(this.store.pipe(select(selectIsExperimentLaunched))),
      filter(([action, isBackCalledOnce]) => !isBackCalledOnce),
      switchMap((action) =>
        this.stimulusService.getFirstStimulus()
      .pipe(
        map((backDatas) =>
          receivedBackAnswer({
            backData: backDatas
          })
        )
    ))));

  responseUserToStimulus$ = createEffect(() =>
    this.actions$.pipe(
      ofType(responseUserToStimulus),
      tap((action) => console.log("responseStimulusEffect trigger")),
      mergeMap((action) =>
        this.stimulusService.sendSubjectAnswer(
          action.responseToStimulus
      ).pipe(
        map((backDatas) =>
          receivedBackAnswer({
            backData: backDatas
          })
        )
      )
    ))
  );


  constructor(
    private actions$: Actions,
    private stimulusService: StimulusService,
    private store: Store<AppState>
  ) {}
}
