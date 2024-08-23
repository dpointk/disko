"use client";

import { Navbar } from "../components/Navbar";
import React from 'react';

export default function About() {
    return (
          <>
    <Navbar />
    <div className="pt-4 min-h-screen" style={{ backgroundImage: 'linear-gradient(120deg, #a1c4fd 0%, #c2e9fb 100%)' }}>
    <div className="pt-4">
            <div className="px-[20px]">
                <h1 className="text-center text-8xl leading-tight font-inter text-[#172026]">
                    About
                </h1>
                <p className="text-center pt-3 text-3xl leading-relaxed max-w-2xl mx-auto mt-15">
                    Disko is an open source tool, designed to manage and facilitate operations in disconnected (air-gapped) environments. It has three main features: Statistics of Images per Registry, Copy Images Between Registries and Migrate Images in Kubernetes.
                </p>
                <div className="flex justify-center mt-9">
                </div>
            </div>
        </div>
        </div>
        </>
    );
}
