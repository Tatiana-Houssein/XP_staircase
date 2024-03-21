import { createAction, props } from '@ngrx/store';
import { BackDatas } from './models';

export const increment = createAction('[App] Increment');

export const userRespondToStimulus = createAction(
  'User respond to stimulus',
  props<{ responseToStimulus: number }>()
);

export const userSendForm = createAction(
  'User send form',
  props<{ responseToStimulus: number }>()
);

export const frontReceiveBackAnswer = createAction(
  '[Source] Event',
  props<{ backData: BackDatas }>()
);

export const startNewExperiment = createAction('Start new expriment');

export const loadExperimentComponent = createAction(
  'Load Experiment component'
);
