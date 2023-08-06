import os,sys,glob,shutil,datetime
import numpy


from .Library_LibraryDependencyList import *
from .Library_FileWriteText import * 
from .Library_FileReadAsText import *

__filedir__=os.path.abspath(os.path.dirname(__file__))



def create_package(
			PackageReadme= True,
			PackageTargetDirectory= ".",
			PackageSourceDirectory= ".",
			PackageName= "",
			PackageAuthor= "",
			PackageDataFileTypes= [],
			PackageDataFolders=[],
			PackageAuthorEmail= "",
			PackageInstallRequires= [],
			IncludeInAPI=[],
			PackageLicense= "",
			PackageURL= "",
			PackageTests= True,
			CreateDocs=True,
			InitAsGit= False,
			ConnectRemoteGitRepository= '',
			CheckArguments = False,
			PrintExtra = False,
			):
	"""
	Used to create a python package skeleton, should come out of the box with
	some bare documentation and be installable/ready to be pip installable.

	Parameters
	----------
	PackageReadme: bool
		If True, a barebones README is created in the base package directory.
	PackageTargetDirectory: str
		The path/name of the save location for your package
	PackageSourceDirectory: str
		The path/name of the folder containing your code
	PackageName: str
		What you want the name of your package to be
	PackageAuthor: str
		Your name (for docs)
	PackageDataFileTypes: list
		List of data file extensions (e.g. txt, dat) for any data files in your code directory
	PackageDataFolders: list
		List of data folders you need included in your package
	PackageAuthorEmail: str
		Author e-mail address for docs
	PackageInstallRequires: list
		By default this package will guess what remote dependencies exist from the code itself,
		this will overwrite that.
	IncludeInAPI: list
		List of your modules you want to run autodoc on (and therefore should be documented so that
		autodoc can read them)
	PackageLicense: str
		Your package license (for docs)
	PackageURL: str
		If your package has a website (for docs)
	PackageTests: bool
		If True, a test script is set up for your package (that you should then edit.)
	CreateDocs: bool
		If True, barebones documentation is created for a readthedocs page.
	InitAsGit: bool
		If True, the new package directory is initialized as a git repository
	ConnectRemoteGitRepository: str
		A remote git repository to connect your local repo to, and adds it to docs install
	CheckArguments: bool
		if true, checks the arguments with conditions written in the function
		if false, ignores those conditions
	PrintExtra: int
		if greater than 0, prints addional information about the function
		if 0, function is expected to print nothing to console
	
	Returns
	-------

	"""
	Result = None

	if (CheckArguments):
		ArgumentErrorMessage = ""

		if len(PackageName) == 0:
			ArgumentErrorMessage += "Must supply a name of your package.\n"

		if not isinstance(PackageDataFileTypes,(list,tuple,numpy.ndarray)):
			PackageDataFileTypes = [PackageDataFileTypes]

		if not isinstance(PackageInstallRequires,(list,tuple,numpy.ndarray)):
			PackageInstallRequires = [PackageInstallRequires]

		if CreateDocs:
			import sphinx_rtd_theme

		if (len(ArgumentErrorMessage) > 0 ):
			if(PrintExtra):
				print("ArgumentErrorMessage:\n", ArgumentErrorMessage)
			raise Exception(ArgumentErrorMessage)

	if os.path.exists(PackageTargetDirectory):
		raise Exception("Package directory %s already exists!!"%PackageTargetDirectory)

	os.makedirs(PackageTargetDirectory)

	ProjectPythonFiles = glob.glob(os.path.join(PackageSourceDirectory,'*.py'))
	ProjectDataFiles = list(numpy.array([glob.glob(os.path.join(PackageSourceDirectory,'*.%s'%fileExtension)) for fileExtension in PackageDataFileTypes]).flatten())
	ProjectPythonFileBasenamesWithoutExtension = [os.path.splitext(os.path.basename(PythonFile))[0] for PythonFile in ProjectPythonFiles]

	ProjectPackageLocalDependencies = []
	ProjectPackageRemoteDependencies = []
	ProjectPackageBuiltinDependencies = []
	ProjectPackageMissingDependencies = []

	ExtraBuiltins = ['traceback','copy','pickle','datetime','os','math','types','random','shutil',
					'pylab','inspect','socket','re','multiprocessing','subprocess','glob']
	for ProjectFileName in ProjectPythonFiles:

		LibraryName = os.path.splitext(ProjectFileName)[0]
		List = Library_LibraryDependencyList(LibraryName = LibraryName,PrintExtra=PrintExtra)

		for ModuleOrPackage in List:
			if len(ModuleOrPackage) == 0 or ModuleOrPackage[0] == '#':
				continue
			if ModuleOrPackage[0] == '.': #This is a relative import
				ModuleOrPackage = ModuleOrPackage[1:]
			ModuleOrPackage = ModuleOrPackage.split('.')[0]
			if numpy.any([ModuleOrPackage in PotentialPackageList for PotentialPackageList in [ProjectPackageRemoteDependencies,
																							ProjectPackageLocalDependencies,
																							ProjectPackageMissingDependencies,
																							ProjectPackageBuiltinDependencies]]):
				#We've already found a place for this Module or Package
				continue
			if PrintExtra:
				print('CHECKING:%s'%ModuleOrPackage)
			if ModuleOrPackage in ProjectPythonFileBasenamesWithoutExtension: #Must be a local dependency
				ProjectPackageLocalDependencies.append(ModuleOrPackage)
			elif ModuleOrPackage in sys.builtin_module_names or '_'+ModuleOrPackage in sys.builtin_module_names or ModuleOrPackage in ExtraBuiltins or len(PackageInstallRequires)>0:
				ProjectPackageBuiltinDependencies.append(ModuleOrPackage)
			elif os.system('pip search %s > /dev/null 2>&1'%ModuleOrPackage)==0 or os.system('conda search %s > /dev/null 2>&1'%ModuleOrPackage)==0: #in either pip or conda
				ProjectPackageRemoteDependencies.append(ModuleOrPackage)
			else:
				ProjectPackageMissingDependencies.append(ModuleOrPackage)
	if len(PackageInstallRequires) > 0:
		ProjectPackageRemoteDependencies = PackageInstallRequires
	if PrintExtra and len(ProjectPackageMissingDependencies) > 0:
		print('Warning: Did not find the following modules/packages, hopefully you know why...{}'.format(ProjectPackageMissingDependencies))
	

	PackageSetupPackages = 'numpy' if 'numpy' in ProjectPackageRemoteDependencies else ''

	if PackageTests and 'astropy' not in ProjectPackageRemoteDependencies:
		ProjectPackageRemoteDependencies.append('astropy')
	if PackageTests and 'pytest-astropy' not in ProjectPackageRemoteDependencies:
		ProjectPackageRemoteDependencies.append('pytest-astropy')
	#Start creating all these files/folders...
	os.makedirs(os.path.join(PackageTargetDirectory,PackageName))
	

	if len(PackageDataFileTypes) == 0:
		PackageData = False
	else:
		PackageData = True

	SetupFileContents=Library_FileReadAsText(os.path.join(__filedir__,'default','setup.py'))
	SetupFileContents=SetupFileContents.replace('PACKAGE_NAME',PackageName)
	SetupFileContents=SetupFileContents.replace('PACKAGE_AUTHOR_EMAIL',PackageAuthorEmail)
	SetupFileContents=SetupFileContents.replace('PACKAGE_AUTHOR_NAME',PackageAuthor)
	SetupFileContents=SetupFileContents.replace('PACKAGE_URL',PackageURL)
	SetupFileContents=SetupFileContents.replace('PACKAGE_LICENSE',PackageLicense)    
	SetupFileContents=SetupFileContents.replace('PACKAGE_INSTALL','{}'.format(ProjectPackageRemoteDependencies))
	SetupFileContents=SetupFileContents.replace('PACKAGE_SETUP',PackageSetupPackages)
	if len(ProjectDataFiles)>0:
		SetupFileContents=SetupFileContents.replace('DATA_FOLDERS','{}'.format(list(numpy.append(PackageDataFolders,'package_data'))))
	else:
		SetupFileContents=SetupFileContents.replace('DATA_FOLDERS','{}'.format(PackageDataFolders))

	ModuleWriteResult = Library_FileWriteText(
			Filepath = os.path.join(PackageTargetDirectory,'setup.py'),
			WriteText = SetupFileContents,
			OverWrite = True,
			PrintExtra=PrintExtra
			)

	if CreateDocs:
		shutil.copytree(os.path.join(__filedir__,'default','docs'),os.path.join(PackageTargetDirectory,'Docs'))
		
		DocsConfigFileContents = Library_FileReadAsText(os.path.join(PackageTargetDirectory,'Docs','source','conf.py'))

		DocsConfigFileContents = DocsConfigFileContents.replace('PROJECT_NAME',PackageName)
		DocsConfigFileContents = DocsConfigFileContents.replace('PACKAGE_COPYRIGHT',str(int(datetime.datetime.now().year))+' '+PackageAuthor)
		DocsConfigFileContents = DocsConfigFileContents.replace('PACKAGE_AUTHOR_NAME',PackageAuthor)


		ModuleWriteResult = Library_FileWriteText(
				Filepath = os.path.join(PackageTargetDirectory,'Docs','source','conf.py'),
				WriteText = DocsConfigFileContents,
				OverWrite = True,
				PrintExtra=PrintExtra
				)

		
		DocsSourceIndex=Library_FileReadAsText(os.path.join(PackageTargetDirectory,'Docs','source','index.rst'))

		DocsSourceIndex=DocsSourceIndex.replace('PACKAGE_NAME',PackageName)
		DocsSourceIndex=DocsSourceIndex.replace('EQUAL_SIGNS','='*(len('Welcome to ')+len(PackageName)))
		ModuleWriteResult = Library_FileWriteText(
				Filepath = os.path.join(PackageTargetDirectory,'Docs','source','index.rst'),
				WriteText = DocsSourceIndex,
				OverWrite = True,PrintExtra=PrintExtra
				)

		if len(IncludeInAPI)>0:
			DocsSourceAPI = ''
			DocsSourceAPI += '#################\n'
			DocsSourceAPI += 'API Documentation\n'
			DocsSourceAPI += '#################\n'
			DocsSourceAPI += '\n'
			DocsSourceAPI += '|\n'
			DocsSourceAPI += '\n'
			DocsSourceAPI += '*'*len(PackageName)+'\n'
			DocsSourceAPI += '%s\n'%PackageName
			DocsSourceAPI += '*'*len(PackageName)+'\n'
			DocsSourceAPI += '\n'
			for pythonFile in IncludeInAPI:
				DocsSourceAPI += '-'*len(pythonFile)+'\n'
				DocsSourceAPI += '%s\n'%pythonFile
				DocsSourceAPI += '-'*len(pythonFile)+'\n'
				DocsSourceAPI += '.. automodule:: %s.%s\n'%(PackageName,pythonFile)
				DocsSourceAPI += '   :members:\n'
				DocsSourceAPI += '\n'
				DocsSourceAPI += '|\n'
				DocsSourceAPI += '\n'
			

			ModuleWriteResult = Library_FileWriteText(
					Filepath = os.path.join(PackageTargetDirectory,'Docs','source','api.rst'),
					WriteText = DocsSourceAPI,
					OverWrite = True,
					PrintExtra=PrintExtra
					)

		DocsSourceInstall=Library_FileReadAsText(os.path.join(PackageTargetDirectory,'Docs','source','install.rst'))
		DocsSourceInstall = DocsSourceInstall.replace('PACKAGE_NAME',PackageName)
		
		if not InitAsGit or len(ConnectRemoteGitRepository) == 0:
			ind=DocsSourceInstall.find('Install latest development version')
			DocsSourceInstall=DocsSourceInstall[:ind]
		else:
			DocsSourceInstall=DocsSourceInstall.replace('GIT_REPOSITORY',ConnectRemoteGitRepository)
			if not PackageTests:
				DocsSourceInstall=DocsSourceInstall.replace('python setup.py test\n','')
			

		ModuleWriteResult = Library_FileWriteText(
				Filepath = os.path.join(PackageTargetDirectory,'Docs','source','install.rst'),
				WriteText = DocsSourceInstall,
				OverWrite = True,PrintExtra=PrintExtra
				)

		DocsExample=Library_FileReadAsText(os.path.join(PackageTargetDirectory,'Docs','source','_examples','plot_package.py'))
		DocsExample = DocsExample.replace('PACKAGE_NAME',PackageName)
		ModuleWriteResult = Library_FileWriteText(
				Filepath = os.path.join(PackageTargetDirectory,'Docs','source','_examples','plot_package.py'),
				WriteText = DocsExample,
				OverWrite = True,PrintExtra=PrintExtra
				)

		shutil.copyfile(os.path.join(__filedir__,'default','.readthedocs.yml'),os.path.join(PackageTargetDirectory,'.readthedocs.yml'))

		pip_requirements=Library_FileReadAsText(os.path.join(PackageTargetDirectory,'Docs','source','requirements.txt'))
		if isinstance(PackageSetupPackages,list):
			pip_requirements=pip_requirements.replace('SETUP_REQUIRES','\n'.join(PackageSetupPackages))
			ModuleWriteResult = Library_FileWriteText(
					Filepath = os.path.join(PackageTargetDirectory,'Docs','source','requirements.txt'),
					WriteText = pip_requirements,
					OverWrite = True,PrintExtra=PrintExtra
					)
		pip_requirements2=Library_FileReadAsText(os.path.join(PackageTargetDirectory,'Docs','source','requirements2.txt'))
		pip_requirements2=pip_requirements2.replace('INSTALL_REQUIRES','\n'.join(ProjectPackageRemoteDependencies))
		ModuleWriteResult = Library_FileWriteText(
				Filepath = os.path.join(PackageTargetDirectory,'Docs','source','requirements2.txt'),
				WriteText = pip_requirements2,
				OverWrite = True,PrintExtra=PrintExtra
				)
	if InitAsGit:
		
		PackageGitIgnore=Library_FileReadAsText(os.path.join(__filedir__,'default','.gitignore'))
		PackageGitIgnore=PackageGitIgnore.replace('PACKAGE_NAME',PackageName)


		ModuleWriteResult = Library_FileWriteText(
			Filepath = os.path.join(PackageTargetDirectory,'.gitignore'),
			WriteText = PackageGitIgnore,
			OverWrite = True,PrintExtra=PrintExtra
			)

		if PackageReadme:
			ModuleWriteResult = Library_FileWriteText(
				Filepath = os.path.join(PackageTargetDirectory,'README.md'),
				WriteText = '#Insert info about %s here!\n'%PackageName,
				OverWrite = True,PrintExtra=PrintExtra
				)


	PackageInitFile=Library_FileReadAsText(os.path.join(__filedir__,'default','__init__.py'))
	importString=''
	for pythonFile in ProjectPythonFiles:
		importString += 'from .%s import *\n'%os.path.splitext(os.path.basename(pythonFile))[0]
	PackageInitFile=PackageInitFile.replace('IMPORT_LIST',importString)
	if not PackageTests:
		ind=PackageInitFile.find('def')
		PackageInitFile=PackageInitFile[:ind]

	ModuleWriteResult = Library_FileWriteText(
		Filepath = os.path.join(PackageTargetDirectory,PackageName,'__init__.py'),
		WriteText = PackageInitFile,
		OverWrite = True,PrintExtra=PrintExtra
		)

	#Copy over files
	for PythonFile in ProjectPythonFiles:
		if os.path.basename(PythonFile).startswith('Example'):
			if not os.path.exists(os.path.join(PackageTargetDirectory,PackageName,'examples')):
				os.makedirs(os.path.join(PackageTargetDirectory,PackageName,'examples'))
			shutil.copyfile(PythonFile,os.path.join(PackageTargetDirectory,PackageName,'examples',os.path.basename(PythonFile)))
		elif os.path.basename(PythonFile).startswith('Test'):
			if not os.path.exists(os.path.join(PackageTargetDirectory,PackageName,'tests')):
				os.makedirs(os.path.join(PackageTargetDirectory,PackageName,'tests'))
			shutil.copyfile(PythonFile,os.path.join(PackageTargetDirectory,PackageName,'tests',os.path.basename(PythonFile)))
		else:
			shutil.copyfile(PythonFile,os.path.join(PackageTargetDirectory,PackageName,os.path.basename(PythonFile)))
	for DataFile in ProjectDataFiles:
		if not os.path.exists(os.path.join(PackageTargetDirectory,PackageName,'package_data')):
			os.makedirs(os.path.join(PackageTargetDirectory,PackageName,'package_data'))
		shutil.copyfile(DataFile,os.path.join(PackageTargetDirectory,PackageName,'package_data',os.path.basename(DataFile)))
	for DataFolder in PackageDataFolders:
		shutil.copytree(os.path.join(PackageSourceDirectory,DataFolder),os.path.join(PackageTargetDirectory,PackageName,DataFolder))

	#Create relative imports
	FilesToMakeRelative = glob.glob(os.path.join(PackageTargetDirectory,PackageName,'*.py'))
	for PythonFile in [os.path.splitext(f)[0] for f in FilesToMakeRelative]:
		if '__init__' in PythonFile:
			continue
		LocalDependencies = Library_LibraryDependencyList(PythonFile,PrintExtra=PrintExtra)
		PythonFileContent = Library_FileReadAsText(PythonFile+'.py')

		for NeedsToBeRelative in LocalDependencies:
			if NeedsToBeRelative not in ProjectPackageLocalDependencies:
				continue

			if PythonFileContent.find('import %s'%NeedsToBeRelative)==-1: #must be a from __ import __ case
				regular = False
			else:
				regular = True

			if regular:
				PythonFileContent = PythonFileContent.replace('import %s'%NeedsToBeRelative,'from .%s import *'%NeedsToBeRelative)                
			else:
				PythonFileContent = PythonFileContent.replace('from %s'%NeedsToBeRelative,'from .%s'%NeedsToBeRelative)

			if '%s.Main'%NeedsToBeRelative in PythonFileContent:
				PythonFileContent = PythonFileContent.replace('%s.Main'%NeedsToBeRelative,NeedsToBeRelative)
			else:
				PythonFileContent = PythonFileContent.replace('%s.'%NeedsToBeRelative,'')

		PythonFileContent = PythonFileContent.replace('def create_package','def %s'%os.path.basename(PythonFile))
		for f in ProjectDataFiles:
			PythonFileContent = PythonFileContent.replace(f,os.path.join('package_data',os.path.basename(f)))
		ModuleWriteResult = Library_FileWriteText(
			Filepath = PythonFile+'.py',
			WriteText = PythonFileContent,
			OverWrite = True, PrintExtra=PrintExtra
			)

	#Generate Package Test File
	if PackageTests:
		PackageTestFile = ''
		PackageTestFile += '##Test File\n'
		PackageTestFile += 'import sys,os,traceback\n'
		PackageTestFile += 'from copy import deepcopy\n'
		PackageTestFile += "sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))\n"
		PackageTestFile += 'import %s\n'%PackageName
		PackageTestFile += '\n'
		PackageTestFile += 'def test_%s():\n'%PackageName
		PackageTestFile += '\tfailed=0\n'
		PackageTestFile += '\ttotal=0\n'
		PackageTestFile += '\t#Fill in tests here.\n'
		PackageTestFile += '\ttry:   \n'
		PackageTestFile += '\t\ttotal+=1 \n'
		PackageTestFile += "\t\tprint('Testing package...',end='')\n"
		PackageTestFile += "\t\tprint('Passed!')\n"
		PackageTestFile += '\texcept Exception as e:\n'
		PackageTestFile += "\t\tprint('Failed')\n"
		PackageTestFile += '\t\tprint(traceback.format_exc())\n'
		PackageTestFile += '\t\t\n'
		PackageTestFile += '\t\tfailed+=1\n'
		PackageTestFile += '\n'
		PackageTestFile += "\tprint('Passed %i/%i tests.'%(total-failed,total))\n"
		PackageTestFile += '\n'
		PackageTestFile += '\treturn\n'
		PackageTestFile += '\n'
		PackageTestFile += "if __name__ == '__main__':\n"
		PackageTestFile += '\ttest_%s()\n'%PackageName

		ModuleWriteResult = Library_FileWriteText(
				Filepath = os.path.join(PackageTargetDirectory,PackageName,'test_%s.py'%PackageName),
				WriteText = PackageTestFile,
				OverWrite = True,PrintExtra=PrintExtra
				)

	if InitAsGit:
		os.system('git --git-dir %s init'%os.path.join(PackageTargetDirectory,'.git'))
		if len(ConnectRemoteGitRepository)>0:
			os.system('git -C %s remote add origin %s'%(os.path.join(PackageTargetDirectory),ConnectRemoteGitRepository))
			os.system('git -C pull')
		os.system('git -C %s add .'%(os.path.join(PackageTargetDirectory)))
		os.system('git -C %s commit -m "First commit."'%os.path.join(PackageTargetDirectory))
		try:
			os.system('git -C %s push -u origin master'%os.path.join(PackageTargetDirectory))
		except:
			os.system('git -C %s push origin master'%os.path.join(PackageTargetDirectory))

	return Result 
