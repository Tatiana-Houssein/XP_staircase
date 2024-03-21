import { initialState } from './app.state';
import { frontReceiveBackAnswer, newTacheInterferenteData } from './actions';
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
        stateMetaExperiment: backData.metaExperimentState,
        currentId: backData.currentId,
        currentFlagIA: backData.currentIaDisplay,
        nextId: backData.nextId,
        isExperimentLaunched: true,
      }
    )
  ),
  on(
    newTacheInterferenteData,
    (state, { tacheInterferenteData }) => (
      console.log('New Tache Interferente Datas', tacheInterferenteData),
      {
        ...state,
        questionInterferente: tacheInterferenteData['question'],
        expectedResultTacheInterferente: tacheInterferenteData['result'],
      }
    )
  )
);
