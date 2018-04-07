import {HttpClient} from "@angular/common/http";
import {Injectable} from "@angular/core";

@Injectable()
export class AuthService {
  constructor(private http: HttpClient) {
  }

  loginUser(credentials) {
    console.log("On submit ", credentials);
    this.http.post("http://localhost:5000/auth/login", credentials).subscribe(res => console.log(res.json()));
  }
}
