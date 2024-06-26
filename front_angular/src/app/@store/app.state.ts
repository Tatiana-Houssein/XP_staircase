import { createFeatureSelector, createSelector } from '@ngrx/store';

export interface AppState {
  isExperimentLaunched: boolean;
  stateMetaExperiment: string;
  currentId: number;
  currentFlagIA: string;
  currentName: string;
  nextId: number;
  questionInterferente: string;
  expectedResultTacheInterferente: number;
}

export const initialState: AppState = {
  isExperimentLaunched: false,
  stateMetaExperiment: 'phase 1',
  currentId: 1,
  currentFlagIA: 'non_vu',
  currentName: 'Initial Name',
  nextId: 2,
  questionInterferente: '',
  expectedResultTacheInterferente: 0,
};

// Feature Selector
export const selectAppState = createFeatureSelector<AppState>('app');

// Selectors
export const selectCurrentId = createSelector(
  selectAppState,
  (state) => state.currentId
);

export const selectNextId = createSelector(
  selectAppState,
  (state) => state.nextId
);

export const selectIsExperimentLaunched = createSelector(
  selectAppState,
  (state) => state.isExperimentLaunched
);

export const selectQuestionInterferente = createSelector(
  selectAppState,
  (state) => state.questionInterferente
);

export const selectResultTacheInterferente = createSelector(
  selectAppState,
  (state) => state.expectedResultTacheInterferente
);

export const selectFlagIA = createSelector(
  selectAppState,
  (state) => state.currentFlagIA
);

export const selectStateMetaExperiment = createSelector(
  selectAppState,
  (state) => state.stateMetaExperiment
);
