// work-item-review.js - SIMPLE WORKING VERSION
VSS.init({
    usePlatformStyles: true,
    usePlatformScripts: true,
    explicitNotifyLoaded: true,
    setupModuleLoader: true
});

VSS.ready(function() {
    console.log("✅ Story Validator Panel is ready!");
    
    const contributionId = VSS.getContribution().id;
    console.log("Contribution ID:", contributionId);
    
    // Register the panel
    VSS.register(contributionId, {
        onLoad: function(contribution) {
            console.log("Panel loaded successfully!");
            document.getElementById('validateBtn').disabled = false;
            showMessage('Ready to validate. Click the button above.', 'loading');
        }
    });
    
    // Setup button click
    document.getElementById('validateBtn').addEventListener('click', function() {
        validateWorkItem();
    });
    
    VSS.notifyLoadSucceeded();
});

async function validateWorkItem() {
    const btn = document.getElementById('validateBtn');
    
    try {
        btn.disabled = true;
        btn.textContent = '⏳ Validating...';
        showMessage('🔍 Getting current work item...', 'loading');
        
        // Get the work item form service
        const workItemFormService = await VSS.getService("ms.vss-work-web.work-item-form");
        
        if (!workItemFormService) {
            throw new Error("Could not connect to work item form");
        }
        
        // Get the CURRENT work item
        const workItemId = await workItemFormService.getId();
        const title = await workItemFormService.getFieldValue('System.Title') || '';
        const description = await workItemFormService.getFieldValue('System.Description') || '';
        
        // Format the story text
        const storyText = `TITLE: ${title}\n\nDESCRIPTION:\n${description}`;
        
        // CALL YOUR BACKEND API (PORT 8000)
        const response = await fetch('http://localhost:8000/validate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                workItemId: workItemId,
                storyText: storyText
            })
        });
        
        if (!response.ok) {
            throw new Error(`API returned ${response.status}`);
        }
        
        const result = await response.json();
        
        // Display the result
        showMessage(
            `<strong>✅ VALIDATION COMPLETE</strong><br><br>` +
            `${result.validation || JSON.stringify(result)}`,
            'success'
        );
        
    } catch (error) {
        console.error('❌ Error:', error);
        showMessage(
            `<strong>❌ ERROR</strong><br>` +
            `${error.message}<br><br>` +
            `Make sure backend is running on port 8000`,
            'error'
        );
    } finally {
        btn.disabled = false;
        btn.textContent = '🤖 Validate with AI Agent';
    }
}

function showMessage(text, type = '') {
    const resultDiv = document.getElementById('result');
    const classMap = {
        'loading': 'loading',
        'success': 'success',
        'error': 'error'
    };
    
    const className = classMap[type] || '';
    resultDiv.innerHTML = `<div class="${className}">${text}</div>`;
}