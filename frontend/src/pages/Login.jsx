import React, { useState } from 'react';
import { api } from '../services/api';
import { useNavigate, Link } from 'react-router-dom';

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await api.login({ email, password });
            navigate('/');
        } catch (err) {
            setError('Credențiale invalide. Încearcă din nou.');
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-slate-50 px-4">
            <div className="max-w-md w-full bg-white p-10 rounded-3xl shadow-xl border border-slate-100">
                <div className="text-center mb-8">
                    <h2 className="text-3xl font-extrabold text-slate-900">Bine ai revenit</h2>
                    <p className="text-slate-500 mt-2">Intră în contul tău FoodSave</p>
                </div>
                {error && <div className="p-3 mb-6 bg-red-50 text-red-600 rounded-xl text-sm font-medium text-center">{error}</div>}
                <form onSubmit={handleSubmit} className="space-y-6">
                    <div>
                        <label className="block text-sm font-semibold text-slate-700 mb-2">Email</label>
                        <input 
                            type="email" 
                            className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-emerald-500 transition-all"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-semibold text-slate-700 mb-2">Parolă</label>
                        <input 
                            type="password" 
                            className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-emerald-500 transition-all"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </div>
                    <button type="submit" className="w-full py-4 bg-emerald-600 text-white rounded-2xl font-bold text-lg hover:bg-emerald-700 transition-all shadow-lg shadow-emerald-200">
                        Autentificare
                    </button>
                </form>
                <div className="mt-8 text-center">
                    <span className="text-slate-500">Nu ai cont? </span>
                    <Link to="/signup" className="text-emerald-600 font-bold hover:underline">Înregistrează-te</Link>
                </div>
            </div>
        </div>
    );
};

export default Login;
