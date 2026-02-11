/**
 * Modern Mestri - Blueprint Designer Logic
 */

let rooms = [];
let nextRoomId = 1;

const designerElements = {
    modal: document.getElementById('designerModal'),
    openBtn: document.getElementById('openDesignerBtn'),
    closeBtn: document.getElementById('closeDesignerBtn'),
    saveBtn: document.getElementById('saveBlueprintBtn'),
    addRoomBtns: document.querySelectorAll('.add-room-btn'),
    roomList: document.getElementById('roomList'),
    canvas: document.getElementById('blueprintCanvas'),
    totalAreaDisplay: document.getElementById('designerTotalArea'),
    mainAreaInput: document.getElementById('area')
};

function setupDesigner() {
    // Open modal
    designerElements.openBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        designerElements.modal.style.display = 'flex';
    });

    // Close modal
    designerElements.closeBtn.addEventListener('click', () => {
        designerElements.modal.style.display = 'none';
    });

    // Add room
    designerElements.addRoomBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            addRoom(btn.dataset.type);
        });
    });

    // Save/Apply
    designerElements.saveBtn.addEventListener('click', () => {
        const totalArea = calculateTotalArea();
        designerElements.mainAreaInput.value = Math.round(totalArea);
        designerElements.modal.style.display = 'none';

        // Store custom layout in global state
        window.customLayout = rooms.map(r => ({
            name: r.name,
            length: r.length,
            width: r.width,
            area: r.length * r.width
        }));
    });
}

function addRoom(type) {
    const room = {
        id: nextRoomId++,
        name: type,
        length: 12,
        width: 10,
        x: 20 + (rooms.length * 40) % 300,
        y: 20 + (rooms.length * 40) % 300
    };

    rooms.push(room);
    renderRoomList();
    renderCanvas();
    updateStats();
}

function renderRoomList() {
    designerElements.roomList.innerHTML = '';
    rooms.forEach(room => {
        const div = document.createElement('div');
        div.className = 'room-item-row';
        div.style.background = 'var(--slate-50)';
        div.style.padding = '0.75rem';
        div.style.borderRadius = '8px';
        div.style.border = '1px solid var(--slate-200)';

        div.innerHTML = `
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="font-weight: 700; font-size: 0.8rem;">${room.name} ${room.id}</span>
                <button onclick="removeRoom(${room.id})" style="color: var(--error); border: none; background: none; cursor: pointer;">&times;</button>
            </div>
            <div style="display: flex; gap: 0.5rem; align-items: center;">
                <input type="number" value="${room.length}" onchange="updateRoom(${room.id}, 'length', this.value)" style="width: 50px; padding: 0.25rem;">
                <span style="font-size: 0.7rem;">L</span>
                <span style="color: var(--slate-300);">×</span>
                <input type="number" value="${room.width}" onchange="updateRoom(${room.id}, 'width', this.value)" style="width: 50px; padding: 0.25rem;">
                <span style="font-size: 0.7rem;">W</span>
                <span style="margin-left: auto; font-size: 0.8rem; font-weight: 800;">${room.length * room.width} <span style="font-weight: 400; font-size: 0.7rem;">sqft</span></span>
            </div>
        `;
        designerElements.roomList.appendChild(div);
    });
}

function renderCanvas() {
    // Clear rooms but keep grid/labels
    const gridLabel = designerElements.canvas.querySelector('div');
    designerElements.canvas.innerHTML = '';
    if (gridLabel) designerElements.canvas.appendChild(gridLabel);

    rooms.forEach(room => {
        const rect = document.createElement('div');
        rect.className = 'canvas-room';
        rect.style.position = 'absolute';
        rect.style.left = room.x + 'px';
        rect.style.top = room.y + 'px';
        rect.style.width = (room.length * 10) + 'px';
        rect.style.height = (room.width * 10) + 'px';
        rect.style.background = 'rgba(29, 78, 216, 0.15)';
        rect.style.border = '2px solid var(--primary)';
        rect.style.borderRadius = '4px';
        rect.style.display = 'flex';
        rect.style.alignItems = 'center';
        rect.style.justifyContent = 'center';
        rect.style.fontSize = '0.6rem';
        rect.style.fontWeight = '700';
        rect.style.color = 'var(--primary)';
        rect.style.textAlign = 'center';
        rect.style.cursor = 'move';
        rect.innerHTML = `<div>${room.name}<br>${room.length}'×${room.width}'</div>`;

        // Simple dragging (mock)
        rect.onmousedown = (e) => {
            let shiftX = e.clientX - rect.getBoundingClientRect().left;
            let shiftY = e.clientY - rect.getBoundingClientRect().top;

            function moveAt(pageX, pageY) {
                let newX = pageX - designerElements.canvas.getBoundingClientRect().left - shiftX;
                let newY = pageY - designerElements.canvas.getBoundingClientRect().top - shiftY;

                // Constraints
                newX = Math.max(0, Math.min(newX, designerElements.canvas.clientWidth - rect.offsetWidth));
                newY = Math.max(0, Math.min(newY, designerElements.canvas.clientHeight - rect.offsetHeight));

                rect.style.left = newX + 'px';
                rect.style.top = newY + 'px';
                room.x = newX;
                room.y = newY;
            }

            function onMouseMove(event) {
                moveAt(event.pageX, event.pageY);
            }

            document.addEventListener('mousemove', onMouseMove);

            document.onmouseup = function () {
                document.removeEventListener('mousemove', onMouseMove);
                document.onmouseup = null;
            };
        };

        rect.ondragstart = function () { return false; };

        designerElements.canvas.appendChild(rect);
    });
}

function updateRoom(id, prop, val) {
    const room = rooms.find(r => r.id === id);
    if (room) {
        room[prop] = parseFloat(val) || 0;
        renderRoomList();
        renderCanvas();
        updateStats();
    }
}

function removeRoom(id) {
    rooms = rooms.filter(r => r.id !== id);
    renderRoomList();
    renderCanvas();
    updateStats();
}

function calculateTotalArea() {
    return rooms.reduce((sum, r) => sum + (r.length * r.width), 0);
}

function updateStats() {
    designerElements.totalAreaDisplay.textContent = Math.round(calculateTotalArea());
}

// Global hook
window.removeRoom = removeRoom;
window.updateRoom = updateRoom;

document.addEventListener('DOMContentLoaded', setupDesigner);
