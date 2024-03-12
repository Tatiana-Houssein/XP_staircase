import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TacheInterferenteComponent } from './forms/tache-interferente/tache-interferente.component';
import { ExperimentComponent } from './experiments/experiment/experiment.component';
import { UserInfoComponent } from './forms/user-info/user-info.component';
import { InfoSecondTaskComponent } from './forms/info-second-task/info-second-task.component';
import { InfoFirstTaskComponent } from './forms/info-first-task/info-first-task.component';
import { InfoThirdTaskComponent } from './forms/info-third-task/info-third-task.component';
import { FormBeginningComponent } from './forms/form-beginning/form-beginning.component';
import { FormEndingComponent } from './forms/form-ending/form-ending.component';

const routes: Routes = [
  { path: '', component: UserInfoComponent },
  { path: 'form-beginning', component: FormBeginningComponent },
  { path: 'form-ending', component: FormEndingComponent },
  { path: 'experiment', component: ExperimentComponent },
  { path: 'calcul-mental', component: TacheInterferenteComponent },
  { path: 'info-first-task', component: InfoFirstTaskComponent },
  { path: 'info-second-task', component: InfoSecondTaskComponent },
  { path: 'info-third-task', component: InfoThirdTaskComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
