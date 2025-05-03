document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const welcomeScreen = document.querySelector('.welcome-screen');
    const assessmentScreen = document.querySelector('.assessment-screen');
    const resultScreen = document.querySelector('.result-screen');
    const questionText = document.querySelector('.question-text');
    const questionImage = document.querySelector('.question-image');
    const optionsContainer = document.querySelector('.options-container');
    const progressBar = document.querySelector('.progress');
    const questionCounter = document.querySelector('.question-counter');
    const prevBtn = document.querySelector('.prev-btn');
    const navLinks = document.querySelectorAll('.nav-link');
    const downloadBtn = document.querySelector('.download-btn');
    
    const pages = {
        home: welcomeScreen,
        chat: document.querySelector('.chat-screen'),
        assessment: assessmentScreen,
        results: resultScreen
    };

    // State
    let currentQuestion = 0;
    let answers = [];
    let doshaScores = { vata: 0, pitta: 0, kapha: 0 };
    let chatHistory = [];
    
    // Questions with specific options and dosha weights
    const questions = [
        {
            question: "What best describes your body frame?",
            image: "🌱",
            options: [
                { text: "Thin and light", dosha: "vata", icon: "🦴" },
                { text: "Medium and muscular", dosha: "pitta", icon: "💪" },
                { text: "Large and solid", dosha: "kapha", icon: "🏋️" }
            ]
        },
        {
            question: "How is your skin typically?",
            image: "🧴",
            options: [
                { text: "Dry, thin, cool", dosha: "vata", icon: "🏜️" },
                { text: "Oily, warm, prone to rashes", dosha: "pitta", icon: "🔥" },
                { text: "Thick, oily, cool", dosha: "kapha", icon: "💧" }
            ]
        },
        {
            question: "How do you handle stress?",
            image: "🧘",
            options: [
                { text: "Worry, anxiety, irregular habits", dosha: "vata", icon: "🌀" },
                { text: "Frustration, anger, intensity", dosha: "pitta", icon: "💢" },
                { text: "Avoidance, withdrawal, lethargy", dosha: "kapha", icon: "🛌" }
            ]
        },
        {
            question: "What's your typical appetite like?",
            image: "🍽️",
            options: [
                { text: "Irregular, often forget to eat", dosha: "vata", icon: "⏱️" },
                { text: "Strong, can't miss meals", dosha: "pitta", icon: "🍗" },
                { text: "Steady, can skip meals easily", dosha: "kapha", icon: "🍎" }
            ]
        },
        {
            question: "How is your sleep typically?",
            image: "🛌",
            options: [
                { text: "Light, interrupted, difficulty falling asleep", dosha: "vata", icon: "👀" },
                { text: "Moderate, wake up easily", dosha: "pitta", icon: "⏰" },
                { text: "Deep, long, hard to wake up", dosha: "kapha", icon: "😴" }
            ]
        },
        {
            question: "What's your typical energy pattern?",
            image: "⚡",
            options: [
                { text: "Bursts of energy, then fatigue", dosha: "vata", icon: "🎢" },
                { text: "Steady energy throughout day", dosha: "pitta", icon: "📈" },
                { text: "Slow starter, enduring energy", dosha: "kapha", icon: "🐢" }
            ]
        }
    ];
    
    // Complete dosha information
    const doshaInfo = {
        vata: {
            description: "Vata types are creative, energetic, and lively. They tend to have thin builds, dry skin, and variable energy levels. When balanced, they're enthusiastic and imaginative, but when imbalanced may experience anxiety or irregular digestion.",
            recommendations: [
                { title: "Diet", content: "Warm, nourishing foods like cooked grains, stews, and nuts. Stay hydrated with warm drinks." },
                { title: "Lifestyle", content: "Maintain regular routines. Gentle exercise like yoga and daily oil massage can help ground your energy." },
                { title: "Balance Tips", content: "Avoid cold foods and environments. Practice grounding meditation and get plenty of rest." }
            ],
            color: "#7FB3D5",
            icon: "🌬️"
        },
        pitta: {
            description: "Pitta types are intense, focused, and driven. They typically have medium builds, warm body temperatures, and strong digestion. When balanced, they're excellent leaders, but when imbalanced may become irritable or perfectionistic.",
            recommendations: [
                { title: "Diet", content: "Cooling foods like sweet fruits, salads, and coconut. Avoid spicy, oily, or fried foods." },
                { title: "Lifestyle", content: "Avoid excessive heat. Practice moderation in all activities. Evening meditation helps cool intensity." },
                { title: "Balance Tips", content: "Spend time in nature, especially near water. Cultivate patience and avoid over-scheduling." }
            ],
            color: "#F5B7B1",
            icon: "🔥"
        },
        kapha: {
            description: "Kapha types are calm, grounded, and nurturing. They usually have solid builds, smooth skin, and steady energy. When balanced, they're loving and supportive, but when imbalanced may become lethargic or resistant to change.",
            recommendations: [
                { title: "Diet", content: "Light, stimulating foods like steamed veggies, legumes, and spices. Minimize dairy and sweets." },
                { title: "Lifestyle", content: "Regular vigorous exercise. Dry brushing before shower helps stimulate circulation." },
                { title: "Balance Tips", content: "Seek variety and new experiences. Wake up early and avoid daytime napping." }
            ],
            color: "#A2D9CE",
            icon: "💧"
        }
    };

    // ======================
    // EVENT LISTENERS
    // ======================
    
    // Navigation
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const page = e.target.dataset.page;
            
            if (page === 'assessment') {
                startAssessment();
            } else {
                switchPage(page);
            }
            
            // Update active state
            navLinks.forEach(navLink => {
                navLink.classList.toggle('active', navLink === e.target);
            });
        });
    });

    // Buttons
    document.querySelector('.begin-btn').addEventListener('click', startAssessment);
    document.querySelectorAll('.back-btn').forEach(btn => btn.addEventListener('click', goBack));
    prevBtn.addEventListener('click', goToPrevQuestion);
    downloadBtn.addEventListener('click', downloadResults);
    document.querySelector('.send-btn').addEventListener('click', sendMessage);
    document.querySelector('.chat-input textarea').addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // ======================
    // CORE FUNCTIONS
    // ======================

    function switchPage(page) {
        // Hide all pages
        Object.values(pages).forEach(pageEl => {
            pageEl.classList.add('hidden');
        });
        
        // Show selected page
        if (pages[page]) {
            pages[page].classList.remove('hidden');
            
            // Special cases
            if (page === 'chat') {
                loadChatHistory();
            }
        }
    }

    function startAssessment() {
        currentQuestion = 0;
        answers = [];
        doshaScores = { vata: 0, pitta: 0, kapha: 0 };
        switchPage('assessment');
        loadQuestion(currentQuestion);
        progressBar.style.width = '0%';
    }

    function loadQuestion(index) {
        if (index < 0 || index >= questions.length) return;
        
        const question = questions[index];
        questionText.textContent = question.question;
        questionImage.textContent = question.image;
        
        // Update progress
        const progress = (index / questions.length) * 100;
        progressBar.style.width = `${progress}%`;
        questionCounter.textContent = `Question ${index + 1} of ${questions.length}`;
        
        // Load options
        optionsContainer.innerHTML = '';
        question.options.forEach((option, i) => {
            const optionBtn = document.createElement('button');
            optionBtn.className = 'option-btn';
            optionBtn.innerHTML = `
                <div class="option-icon">${option.icon}</div>
                <div>${option.text}</div>
            `;
            
            if (answers[index] === i) {
                optionBtn.classList.add('selected');
            }
            
            optionBtn.addEventListener('click', () => selectOption(index, i));
            optionsContainer.appendChild(optionBtn);
        });
        
        prevBtn.style.visibility = index === 0 ? 'hidden' : 'visible';
    }

    function selectOption(questionIndex, optionIndex) {
        optionsContainer.querySelectorAll('.option-btn').forEach(btn => {
            btn.classList.remove('selected');
        });
        
        const selectedBtn = optionsContainer.children[optionIndex];
        selectedBtn.classList.add('selected');
        answers[questionIndex] = optionIndex;
        
        setTimeout(() => {
            goToNextQuestion();
        }, 500);
    }

    function goToNextQuestion() {
        if (answers[currentQuestion] === undefined) {
            showValidationMessage("Please select an option to continue");
            return;
        }
        
        const selectedOption = questions[currentQuestion].options[answers[currentQuestion]];
        doshaScores[selectedOption.dosha] += 1;
        
        const progress = ((currentQuestion + 1) / questions.length) * 100;
        progressBar.style.width = `${progress}%`;
        
        if (currentQuestion < questions.length - 1) {
            currentQuestion++;
            loadQuestion(currentQuestion);
        } else {
            showResults();
        }
    }

    function goToPrevQuestion() {
        if (currentQuestion > 0) {
            // Remove previous answer's score
            if (answers[currentQuestion] !== undefined) {
                const prevOption = questions[currentQuestion].options[answers[currentQuestion]];
                doshaScores[prevOption.dosha] -= 1;
            }
            
            currentQuestion--;
            loadQuestion(currentQuestion);
        }
    }

    function showResults() {
        // Include the last question's answer if not already counted
        if (answers[currentQuestion] !== undefined && currentQuestion === questions.length - 1) {
            const selectedOption = questions[currentQuestion].options[answers[currentQuestion]];
            doshaScores[selectedOption.dosha] += 1;
        }

        switchPage('results');
        
        const dominantDosha = Object.entries(doshaScores).reduce((a, b) => 
            a[1] > b[1] ? a : b
        )[0];
        
        const doshaData = doshaInfo[dominantDosha];
        
        document.querySelector('.dosha-title').textContent = 
            `${dominantDosha.charAt(0).toUpperCase() + dominantDosha.slice(1)} Dominant`;
        document.querySelector('.dosha-description').textContent = doshaData.description;
        document.querySelector('.result-icon').style.backgroundColor = doshaData.color;
        document.querySelector('.result-icon').textContent = doshaData.icon;
        
        // Update stats bars
        const totalQuestions = questions.length;
        Object.entries(doshaScores).forEach(([dosha, score]) => {
            const percentage = Math.round((score / totalQuestions) * 100);
            const bar = document.querySelector(`.stat-bar.${dosha}`);
            const value = document.querySelector(`.stat-bar.${dosha} + .stat-value`);
            
            setTimeout(() => {
                bar.style.height = `${percentage}%`;
                value.textContent = `${percentage}%`;
            }, 100);
        });
        
        // Add recommendations
        const recommendationsContainer = document.querySelector('.recommendation-cards');
        recommendationsContainer.innerHTML = '';
        
        doshaData.recommendations.forEach(rec => {
            const card = document.createElement('div');
            card.className = 'recommendation-card';
            card.innerHTML = `
                <h5>${rec.title}</h5>
                <p>${rec.content}</p>
            `;
            recommendationsContainer.appendChild(card);
        });
        
        triggerConfetti();
    }

    function triggerConfetti() {
        const count = 200;
        const defaults = {
            origin: { y: 0.7 },
            colors: ['#2A5934', '#D4A96A', '#9C4A1A', '#7FB3D5', '#F5B7B1', '#A2D9CE']
        };
        
        function fire(particleRatio, opts) {
            confetti({
                ...defaults,
                ...opts,
                particleCount: Math.floor(count * particleRatio)
            });
        }
        
        fire(0.25, { spread: 26, startVelocity: 55 });
        fire(0.2, { spread: 60 });
        fire(0.35, { spread: 100, decay: 0.91, scalar: 0.8 });
        fire(0.1, { spread: 120, startVelocity: 25, decay: 0.92, scalar: 1.2 });
        fire(0.1, { spread: 120, startVelocity: 45 });
    }

async function downloadResults() {
    const { jsPDF } = window.jspdf;
    const resultContent = document.querySelector('.result-content');
    const doshaTitle = document.querySelector('.dosha-title').textContent.replace(/\s+/g, '_');

    const canvas = await html2canvas(resultContent, { scale: 2 });
    const imgData = canvas.toDataURL('image/png');

    const pdf = new jsPDF({
        orientation: 'portrait',
        unit: 'pt',
        format: 'a4'
    });

    const pdfWidth = pdf.internal.pageSize.getWidth();
    const pdfHeight = pdf.internal.pageSize.getHeight();

    // Calculate image dimensions to fit within PDF page while maintaining aspect ratio
    const imgProps = pdf.getImageProperties(imgData);
    const imgWidth = pdfWidth * 0.9;
    const imgHeight = (imgProps.height * imgWidth) / imgProps.width;

    let position = 20; // top margin

    pdf.addImage(imgData, 'PNG', (pdfWidth - imgWidth) / 2, position, imgWidth, imgHeight);
    pdf.save(`Ayurvedic_Results_${doshaTitle}.pdf`);
}

    function showValidationMessage(message) {
        const validationEl = document.querySelector('.validation-message');
        validationEl.textContent = message;
        validationEl.classList.add('animate__animated', 'animate__headShake');
        
        setTimeout(() => {
            validationEl.classList.remove('animate__animated', 'animate__headShake');
        }, 1000);
    }

    function goBack() {
        if (resultScreen.classList.contains('hidden')) {
            switchPage('home');
        } else {
            startAssessment();
        }
    }

    // ======================
    // CHAT FUNCTIONS
    // ======================

    async function loadChatHistory() {
        try {
            const response = await fetch('/api/chat/history');
            const data = await response.json();
            chatHistory = data;
            
            const messagesContainer = document.querySelector('.chat-messages');
            messagesContainer.innerHTML = '';
            
            data.forEach(msg => {
                addMessage(msg.message, msg.sender);
            });
        } catch (error) {
            console.error('Error loading chat history:', error);
        }
    }

    async function sendMessage() {
        const input = document.querySelector('.chat-input textarea');
        const message = input.value.trim();
        
        if (!message) return;
        
        addMessage(message, 'user');
        input.value = '';
        
        try {
            const typingIndicator = addTypingIndicator();
            
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({message})
            });
            
            if (!response.ok) throw new Error('API request failed');
            
            const data = await response.json();
            typingIndicator.remove();
            addMessage(data.response, 'bot');
            
        } catch (error) {
            document.querySelector('.typing-indicator')?.remove();
            addMessage("Sorry, I'm having trouble connecting. Please try again later.", 'bot');
        }
    }

function addMessage(text, sender) {
    const messagesContainer = document.querySelector('.chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `${sender}-message`;
    
    if (sender === 'bot') {
        messageDiv.innerHTML = `
            <div class="message-content">
                <div class="bot-icon">🌿</div>
                <div class="message-text">${marked.parse(text)}</div>
            </div>
        `;
        
        // Add quick reply button if text includes 'assessment'
        if (text.includes('assessment')) {
            const quickRepliesDiv = document.createElement('div');
            quickRepliesDiv.className = 'quick-replies';
            const button = document.createElement('button');
            button.className = 'quick-reply';
            button.textContent = 'Begin Assessment';
            button.addEventListener('click', () => startAssessment());
            quickRepliesDiv.appendChild(button);
            messageDiv.querySelector('.message-text').appendChild(quickRepliesDiv);
        }
    } else {
        messageDiv.innerHTML = `
            <div class="message-content">
                <div class="message-text">${marked.parse(text)}</div>
            </div>
        `;
    }
    
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

    function addTypingIndicator() {
        const messagesContainer = document.querySelector('.chat-messages');
        const typingDiv = document.createElement('div');
        typingDiv.className = 'bot-message typing-indicator';
        typingDiv.innerHTML = `
            <div class="message-content">
                <div class="bot-icon">🌿</div>
                <div class="message-text">
                    <div class="typing-dots">
                        <span></span>
                        <span></span>
                        <span></span>
                    </div>
                </div>
            </div>
        `;
        messagesContainer.appendChild(typingDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        return typingDiv;
    }

    // Initialize
    switchPage('home');
    
    // Load html2canvas dynamically
    const script = document.createElement('script');
    script.src = 'https://html2canvas.hertzen.com/dist/html2canvas.min.js';
    document.head.appendChild(script);
});