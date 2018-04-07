import {Component} from '@angular/core';
import {AuthService} from "./services/auth.service";
import {AutobahnService} from "./services/autobahn.service";

export interface User {
  id: string;
  email: string;
  password: string;
  token: string;
}

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'Crossbar Test App';
  user: User = {
    id: null,
    email: "robinnagpal.tiet@gmail.com",
    password: "secret",
    token: null
  };

  constructor(
    private authService: AuthService,
    private autobahnService: AutobahnService
  ) {
    this.authService = authService;
    this.autobahnService = autobahnService;
  }

  onLogin() {
    this.authService.loginUser(this.user).subscribe((res: User) => this.user = res);
  }

  connectToWamp() {
    this.autobahnService.connectToWamp(this.user.id, this.user.token);
  }
}
