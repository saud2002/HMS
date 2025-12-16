#!/usr/bin/env python3
"""
Update Doctors Frontend to Use Database API
"""
import re
from pathlib import Path

def update_doctors_html():
    """Update doctors.html to use API"""
    file_path = Path("frontend/doctors.html")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update renderDoctors function
    old_render = r'function renderDoctors\(list = null\) \{[^}]+\}'
    new_render = '''async function renderDoctors(list = null) {
            try {
                const doctors = list || await API.Doctors.getAll();
                document.getElementById('doctorsTable').innerHTML = doctors.map(d => `
                    <tr>
                        <td>${d.doctor_id}</td>
                        <td>${d.doctor_name}</td>
                        <td>${d.specialization}</td>
                        <td>Rs. ${d.consultation_charges.toLocaleString()}</td>
                        <td><span class="status-badge status-${d.status.toLowerCase()}">${d.status}</span></td>
                        <td>
                            <button class="btn btn-sm btn-primary" onclick="openDoctorModal('${d.doctor_id}')">Edit</button>
                            <button class="btn btn-sm btn-secondary" onclick="toggleDoctorStatus('${d.doctor_id}')">${d.status === 'Active' ? 'Deactivate' : 'Activate'}</button>
                        </td>
                    </tr>
                `).join('') || '<tr><td colspan="6" style="text-align:center;">No doctors found</td></tr>';
            } catch (error) {
                console.error('Error loading doctors:', error);
                document.getElementById('doctorsTable').innerHTML = '<tr><td colspan="6" style="text-align:center; color: red;">Error loading doctors</td></tr>';
            }
        }'''
    
    # Replace the function (this is a simplified approach)
    # Let's find and replace specific parts
    
    # Replace HMS.doctors.getAll() with API call
    content = re.sub(r'HMS\.doctors\.getAll\(\)', 'await API.Doctors.getAll()', content)
    
    # Replace function declaration
    content = re.sub(r'function renderDoctors\(', 'async function renderDoctors(', content)
    
    # Replace field names
    content = re.sub(r'\$\{d\.id\}', '${d.doctor_id}', content)
    content = re.sub(r'\$\{d\.name\}', '${d.doctor_name}', content)
    content = re.sub(r'\$\{d\.fee\}', '${d.consultation_charges.toLocaleString()}', content)
    
    # Add error handling
    if 'try {' not in content:
        # Add basic error handling structure
        content = content.replace(
            'const doctors = list || await API.Doctors.getAll();',
            '''try {
                const doctors = list || await API.Doctors.getAll();'''
        )
        content = content.replace(
            '|| \'<tr><td colspan="6" style="text-align:center;">No doctors found</td></tr>\';',
            '''|| '<tr><td colspan="6" style="text-align:center;">No doctors found</td></tr>';
            } catch (error) {
                console.error('Error loading doctors:', error);
                document.getElementById('doctorsTable').innerHTML = '<tr><td colspan="6" style="text-align:center; color: red;">Error loading doctors</td></tr>';
            }'''
        )
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Updated doctors.html")

def main():
    """Main function"""
    print("🔧 Updating Doctors Frontend")
    print("=" * 30)
    
    update_doctors_html()
    
    print("✅ Doctors frontend updated!")

if __name__ == "__main__":
    main()