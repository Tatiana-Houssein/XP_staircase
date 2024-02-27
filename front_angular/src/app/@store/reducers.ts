import { initialState } from './app.state';
import { frontReceiveBackAnswer } from './actions';
import { increment } from './actions';

import { createReducer, on } from '@ngrx/store';

export const appReducer = createReducer(
  initialState,
  on(increment, (state) => ({
    ...state,
    currentId: state.currentId + 1,
    nextId: state.nextId + 1,
  })),
  on(
    frontReceiveBackAnswer,
    (state, { backData }) => (
      console.log('RECEIVING BACK DATAS', backData),
      {
        ...state,
        stateMetaExperiment: backData.stateMetaExperiment,
        currentId: backData.currentId,
        currentFlagIA: backData.currentIaDisplay,
        nextId: backData.nextId,
        questionInterferente: state.nextQuestionInterferente,
        nextQuestionInterferente: backData.questionInterferente,
        isExperimentLaunched: true,
      }
    )
  )
);
