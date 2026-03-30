import React from 'react'
import { MapPin, ShoppingBag, Heart, Menu } from 'lucide-react'

function App() {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-800">
      {/* Navigation */}
      <nav className="sticky top-0 bg-white/80 backdrop-blur-md border-b z-50">
        <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Heart className="text-emerald-500 fill-emerald-500" />
            <span className="text-xl font-bold tracking-tight">Food<span className="text-emerald-600">Save</span></span>
          </div>
          <div className="hidden md:flex items-center gap-8 font-medium italic">
            <a href="#" className="text-emerald-600">Home</a>
            <a href="#" className="hover:text-emerald-600 transition-colors">Explore Map</a>
            <a href="#" className="hover:text-emerald-600 transition-colors">How it works</a>
          </div>
          <div className="flex items-center gap-4">
            <button className="px-4 py-2 text-sm font-semibold text-emerald-600 hover:bg-emerald-50 rounded-full transition-colors">
              Login
            </button>
            <button className="px-4 py-2 text-sm font-semibold text-white bg-emerald-600 hover:bg-emerald-700 rounded-full shadow-lg shadow-emerald-200 transition-all">
              Sign Up
            </button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="max-w-7xl mx-auto px-4 py-12 md:py-24">
        <div className="text-center space-y-6 max-w-3xl mx-auto">
          <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight text-slate-900 leading-tight">
            Stop Waste. <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-600 to-teal-500">
              Share Surplus.
            </span>
          </h1>
          <p className="text-xl text-slate-600 leading-relaxed">
            Connecting local restaurants and shops with NGOs and communities to ensure no good meal goes to waste.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
            <button className="w-full sm:w-auto px-8 py-4 bg-emerald-600 text-white rounded-2xl font-bold text-lg hover:scale-105 active:scale-95 transition-all shadow-xl shadow-emerald-200">
              Donate Food
            </button>
            <button className="w-full sm:w-auto px-8 py-4 bg-white border-2 border-slate-200 text-slate-700 rounded-2xl font-bold text-lg hover:border-emerald-600 hover:text-emerald-600 transition-all">
              Find Meals
            </button>
          </div>
        </div>

        {/* Feature Grid */}
        <section className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-24">
          <div className="p-8 bg-white rounded-3xl shadow-sm border border-slate-100 hover:shadow-xl hover:shadow-slate-200 transition-all group">
            <div className="w-14 h-14 bg-orange-50 rounded-2xl flex items-center justify-center mb-6 ring-1 ring-orange-100 group-hover:bg-orange-500 group-hover:text-white transition-all">
              <ShoppingBag size={28} />
            </div>
            <h3 className="text-2xl font-bold mb-3">Discounts</h3>
            <p className="text-slate-600">Individual users can buy perfectly good surplus food at massive discounts.</p>
          </div>

          <div className="p-8 bg-white rounded-3xl shadow-sm border border-slate-100 hover:shadow-xl hover:shadow-slate-200 transition-all group">
            <div className="w-14 h-14 bg-emerald-50 rounded-2xl flex items-center justify-center mb-6 ring-1 ring-emerald-100 group-hover:bg-emerald-500 group-hover:text-white transition-all">
              <Heart size={28} />
            </div>
            <h3 className="text-2xl font-bold mb-3">Donations</h3>
            <p className="text-slate-600">NGOs and care centers can claim free food donations from local merchants.</p>
          </div>

          <div className="p-8 bg-white rounded-3xl shadow-sm border border-slate-100 hover:shadow-xl hover:shadow-slate-200 transition-all group">
            <div className="w-14 h-14 bg-blue-50 rounded-2xl flex items-center justify-center mb-6 ring-1 ring-blue-100 group-hover:bg-blue-500 group-hover:text-white transition-all">
              <MapPin size={28} />
            </div>
            <h3 className="text-2xl font-bold mb-3">Interactive Map</h3>
            <p className="text-slate-600">Real-time view of available items near you with precise geolocation.</p>
          </div>
        </section>
      </main>
    </div>
  )
}

export default App
