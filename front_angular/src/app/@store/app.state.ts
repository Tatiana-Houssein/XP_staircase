import { createFeatureSelector, createSelector } from '@ngrx/store';

export interface AppState {
  isExperimentLaunched: boolean;
  currentId: number;
  currentFlagIA: string;
  currentName: string;
  nextId: number;
  questionInterferente: string;
  nextQuestionInterferente: string;
}

export const initialState: AppState = {
  isExperimentLaunched: false,
  currentId: 1,
  currentFlagIA: "non_vu",
  currentName: 'Initial Name',
  nextId: 2,
  questionInterferente: "",
  nextQuestionInterferente: "",
};

// Feature Selector
export const selectAppState = createFeatureSelector<AppState>('app');

// Selectors
export const selectCurrentId = createSelector(selectAppState, (state) => state.currentId);

export const selectNextId = createSelector(selectAppState, (state) => state.nextId);

export const selectIsExperimentLaunched = createSelector(selectAppState, (state) => state.isExperimentLaunched);

export const selectQuestionInterferente = createSelector(selectAppState, (state) => state.questionInterferente);

export const selectFlagIA = createSelector(selectAppState, (state) => state.currentFlagIA);
