import streamlit as st

st.set_page_config(
    page_title="HydroTransparent - Where Every Drop Tells a Story",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for the split-screen cinematic experience with your images
st.markdown("""
<style>
    /* Base styles */
    .main {
        background: #000000;
        color: white;
        font-family: 'Inter', sans-serif;
    }
    
    /* Split screen containers */
    .split-screen {
        display: flex;
        height: 100vh;
        position: relative;
        overflow: hidden;
    }
    
    .problem-side {
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.7)), 
                    url('https://citizenjusticenetwork.org/wp-content/uploads/2016/02/water-1080x675.jpg');
        background-size: cover;
        background-position: center;
        transition: all 1.5s ease;
        position: relative;
    }
    
    .solution-side {
        background: linear-gradient(rgba(0,180,219,0.2), rgba(0,180,219,0.3)), 
                    url('https://drinkoptimum.com/wp-content/uploads/water-crisis-optimum.jpg');
        background-size: cover;
        background-position: center;
        transition: all 1.5s ease;
        position: relative;
    }
    
    /* Content styling */
    .side-content {
        padding: 80px 40px;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        position: relative;
        z-index: 2;
    }
    
    .problem-content {
        text-align: right;
        padding-right: 60px;
    }
    
    .solution-content {
        text-align: left;
        padding-left: 60px;
    }
    
    .crisis-label {
        font-size: 1.2rem;
        font-weight: 300;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-bottom: 20px;
        opacity: 0.8;
    }
    
    .solution-label {
        font-size: 1.2rem;
        font-weight: 300;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-bottom: 20px;
        opacity: 0.8;
    }
    
    .headline {
        font-size: 3.5rem;
        font-weight: 700;
        line-height: 1.1;
        margin-bottom: 30px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    .problem-headline {
        color: #ff6b6b;
    }
    
    .solution-headline {
        color: #00b4db;
    }
    
    .subtext {
        font-size: 1.4rem;
        font-weight: 300;
        line-height: 1.6;
        opacity: 0.9;
        max-width: 400px;
    }
    
    /* Final impact section */
    .impact-section {
        background: linear-gradient(135deg, #00b4db 0%, #0083b0 100%);
        padding: 100px 40px;
        text-align: center;
    }
    
    .impact-headline {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 50px;
        color: white;
    }
    
    .impact-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 40px;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .impact-item {
        background: rgba(255,255,255,0.15);
        padding: 30px 20px;
        border-radius: 15px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .impact-number {
        font-size: 3.5rem;
        font-weight: 800;
        color: white;
        margin-bottom: 10px;
    }
    
    .impact-label {
        font-size: 1.1rem;
        font-weight: 400;
        color: rgba(255,255,255,0.9);
    }
    
    .cta-section {
        background: #000000;
        padding: 80px 40px;
        text-align: center;
    }
    
    .cta-headline {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 30px;
        color: white;
    }
    
    .nav-button {
        background: linear-gradient(45deg, #00b4db, #0083b0);
        color: white;
        border: none;
        padding: 15px 30px;
        border-radius: 25px;
        font-size: 1.1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        margin: 10px;
        width: 200px;
    }
    
    .nav-button:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 20px rgba(0,180,219,0.3);
    }
    
    .button-grid {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 15px;
        margin: 30px 0;
    }
    
    .button-label {
        text-align: center;
        color: #ccc;
        font-size: 0.9rem;
        margin-top: 5px;
    }
    
    /* Scroll indicator */
    .scroll-indicator {
        position: absolute;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%);
        color: rgba(255,255,255,0.7);
        font-size: 0.9rem;
        animation: bounce 2s infinite;
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% {transform: translateY(0) translateX(-50%);}
        40% {transform: translateY(-10px) translateX(-50%);}
        60% {transform: translateY(-5px) translateX(-50%);}
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .split-screen {
            flex-direction: column;
            height: auto;
        }
        
        .problem-side, .solution-side {
            flex: 1 !important;
            min-height: 50vh;
        }
        
        .side-content {
            padding: 40px 20px;
        }
        
        .problem-content {
            text-align: center;
            padding-right: 20px;
        }
        
        .solution-content {
            text-align: center;
            padding-left: 20px;
        }
        
        .headline {
            font-size: 2.5rem;
        }
        
        .impact-grid {
            grid-template-columns: 1fr;
            gap: 20px;
        }
        
        .button-grid {
            flex-direction: column;
            align-items: center;
        }
        
        .nav-button {
            width: 100%;
            max-width: 300px;
        }
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Section 1: 70% Problem / 30% Solution
    st.markdown("""
    <div class="split-screen">
        <div class="problem-side" style="flex: 7;">
            <div class="side-content problem-content">
                <div class="crisis-label">The Crisis</div>
                <div class="headline problem-headline">Corruption drains hope</div>
                <div class="subtext">Every missing rand means fewer jobs, fewer projects, fewer drops of water for those who need it most.</div>
            </div>
        </div>
        <div class="solution-side" style="flex: 3;">
            <div class="side-content solution-content">
                <div class="solution-label">The Solution</div>
                <div class="subtext" style="font-size: 1.1rem;">We track every rand with tamper-proof blockchain technology</div>
            </div>
        </div>
        <div class="scroll-indicator">Scroll down to continue the story</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Section 2: 50% Problem / 50% Solution  
    st.markdown("""
    <div class="split-screen">
        <div class="problem-side" style="flex: 5;">
            <div class="side-content problem-content">
                <div class="headline problem-headline">Families walk kilometers</div>
                <div class="subtext">For clean water that should be their basic right. The journey for water steals time, health, and opportunity.</div>
            </div>
        </div>
        <div class="solution-side" style="flex: 5;">
            <div class="side-content solution-content">
                <div class="headline solution-headline">We bring water to them</div>
                <div class="subtext">Solar boreholes, smart treatment pods, and sustainable infrastructure right where it's needed.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Section 3: 30% Problem / 70% Solution
    st.markdown("""
    <div class="split-screen">
        <div class="problem-side" style="flex: 3;">
            <div class="side-content problem-content">
                <div class="subtext" style="font-size: 1.1rem;">Every missing rand is a lost job, a child out of school, a community without hope</div>
            </div>
        </div>
        <div class="solution-side" style="flex: 7;">
            <div class="side-content solution-content">
                <div class="headline solution-headline">We create 450+ jobs per project</div>
                <div class="subtext">Sustainable local employment that builds skills, economy, and community pride for generations.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Final Impact Section
    st.markdown("""
    <div class="impact-section">
        <div class="impact-headline">Transparency is the Source</div>
        <div class="impact-grid">
            <div class="impact-item">
                <div class="impact-number">42% → 85%</div>
                <div class="impact-label">Water Access Improvement</div>
            </div>
            <div class="impact-item">
                <div class="impact-number">30%</div>
                <div class="impact-label">Cost Reduction Through Transparency</div>
            </div>
            <div class="impact-item">
                <div class="impact-number">450+</div>
                <div class="impact-label">Sustainable Jobs Per Project</div>
            </div>
            <div class="impact-item">
                <div class="impact-number">ZAR 85M</div>
                <div class="impact-label">Annual Local Economic Stimulus</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Call to Action Section
    st.markdown("""
    <div class="cta-section">
        <div class="cta-headline">Ready to Build a Water-Secure Future?</div>
        <p style="font-size: 1.3rem; color: #ccc; margin-bottom: 40px; max-width: 600px; margin-left: auto; margin-right: auto;">
            Use the sidebar navigation to explore all features of our comprehensive water solution platform.
        </p>
        
        <div style="background: rgba(255,255,255,0.1); padding: 30px; border-radius: 15px; max-width: 800px; margin: 0 auto;">
            <h3 style="color: #00b4db; text-align: center; margin-bottom: 20px;">🚀 Quick Start Guide</h3>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; text-align: left;">
                <div>
                    <h4 style="color: #00b4db;">1. Start Here:</h4>
                    <p style="color: #ccc; font-size: 0.9rem;">👉 Click <strong>"🏠 Province Map"</strong> in the sidebar to begin with geographic data exploration</p>
                </div>
                <div>
                    <h4 style="color: #00b4db;">2. Then Explore:</h4>
                    <p style="color: #ccc; font-size: 0.9rem;">💧 <strong>Water Solutions</strong> - Engineering options<br>
                    💰 <strong>Cost Calculator</strong> - Project budgeting<br>
                    📊 <strong>Water Quality</strong> - SAN 241 compliance</p>
                </div>
            </div>
        </div>
        
        <div style="margin-top: 40px;">
            <h4 style="color: #00b4db; margin-bottom: 20px;">All Features Available in Sidebar:</h4>
            <div class="button-grid">
                <div>
                    <div style="text-align: center;">
                        <div style="font-size: 2rem; margin-bottom: 10px;">🌍</div>
                        <div class="button-label">Province Map</div>
                    </div>
                </div>
                <div>
                    <div style="text-align: center;">
                        <div style="font-size: 2rem; margin-bottom: 10px;">💧</div>
                        <div class="button-label">Water Solutions</div>
                    </div>
                </div>
                <div>
                    <div style="text-align: center;">
                        <div style="font-size: 2rem; margin-bottom: 10px;">🔧</div>
                        <div class="button-label">3D Equipment</div>
                    </div>
                </div>
                <div>
                    <div style="text-align: center;">
                        <div style="font-size: 2rem; margin-bottom: 10px;">💰</div>
                        <div class="button-label">Cost Calculator</div>
                    </div>
                </div>
                <div>
                    <div style="text-align: center;">
                        <div style="font-size: 2rem; margin-bottom: 10px;">📊</div>
                        <div class="button-label">Water Quality</div>
                    </div>
                </div>
                <div>
                    <div style="text-align: center;">
                        <div style="font-size: 2rem; margin-bottom: 10px;">📋</div>
                        <div class="button-label">Transparency</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Simple instruction for sidebar navigation
    st.markdown("""
    <div style="text-align: center; margin-top: 30px; padding: 20px; background: rgba(0,180,219,0.1); border-radius: 10px;">
        <p style="color: #00b4db; font-size: 1.1rem; font-weight: 600;">
            💡 <strong>Navigation Tip:</strong> Look for the sidebar on the left side of your screen and click any page to explore!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #e0f7fa; font-style: italic; padding: 40px 20px;'>
        <p style='font-size: 1.1rem;'>"When every rand is traceable, corruption cannot hide. When every transaction is public, trust is rebuilt.</p>
        <p style='font-size: 1.1rem;'>When communities can see where money flows, hope returns. This is the HydroTransparent promise."</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
