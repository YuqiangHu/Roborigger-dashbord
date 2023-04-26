import Layout from '../components/layout';

const HomePage = () => {
	return (
		<Layout title='Roborigger | Home' content='Home page'>
			<h1 className='mb-5'>About</h1>
			<p>The scope of this project is to create a PDF report generator running on Django. The MVP will be able to gather data based on the given CSV, and it can generate reports automatically</p>
			<br/>
			<h1 className='mb-5'>User Manual</h1>
			<ul>
			<li><h3>Step One: Register</h3>

			<p>Input the First Name & Last Name & Email and Password</p>
			<p>Password must be at least 8 characters, can not be fully digits</p>
			<p>Then the user gets their account.</p></li>

			<li><h3>Step Two: Login</h3> 

			<p>Use the email and password to sign in to the Roborigger Report Maker.</p>
			<p>Users can tick the Remember Me to record their account information on the website.</p></li>

			<li><h3>Step Three: Generate Monthly report</h3>

			<p>Download CSV file from Roborigger Dashboard (message data) If you cannot access to the Roborigger Dashboard. The sample data can be found in our Teams: Testing data which is a real data from AR10-010 22 Aug - 20 Sep.</p>
			<p>Click file upload box to select file from computer.</p>
			<p>Click Upload Data File button to upload file.</p>
			<p>Click Create Plots button to create plots.</p>
			<p>After the plots are created, click *Create PDF button to generate PDF.</p>
			<p>Input basic information about the unit.</p>
			<p>Preview the generated report.</p>
			<p>Click the 'Save PDF' button to save report to the device.</p></li>


			</ul>
			
					
					
		
		</Layout>
	);
};

export default HomePage;