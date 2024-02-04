import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TacheInterferenteComponent } from './forms/tache-interferente/tache-interferente.component';
import { ExperimentComponent } from './experiments/experiment/experiment.component';
import { UserInfoComponent } from './forms/user-info/user-info.component';

const routes: Routes = [
  { path: '', component: UserInfoComponent },
  { path: 'experiment', component: ExperimentComponent },
  { path: 'calcul-mental', component: TacheInterferenteComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
