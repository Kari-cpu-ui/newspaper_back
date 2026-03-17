import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Usuario {
    id: number;
    name: string;
    email: string;
    role: 'editor' | 'redactor' | 'admin';
    createdAt: string;
}

@Injectable({
  providedIn: 'root',
})
export class UsersService {
    private apiUrl = 'http://127.0.0.1:8000/users/';
    constructor(private http: HttpClient) {}

    getUsers(): Observable<Usuario[]> {
        return this.http.get<Usuario[]>(this.apiUrl);
    }   
}