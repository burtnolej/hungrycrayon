<?php
// Load the main class
require_once 'HTML/QuickForm2.php';
// Load the controller
require_once 'HTML/QuickForm2/Controller.php';
// Load the Action interface (we will implement it)
require_once 'HTML/QuickForm2/Controller/Action.php';

// Class representing a form page
class TutorialPage extends HTML_QuickForm2_Controller_Page
{
    protected function populateForm()
    {
        // Add some elements to the form
        $fieldset = $this->form->addElement('fieldset')->setLabel('QuickForm2_Controller tutorial example');
        $name = $fieldset->addElement('text', 'name', array('size' => 50, 'maxlength' => 255))
                         ->setLabel('Enter your name:');

        // We set the name of the submit button so that it binds to default 'submit' handler
        $fieldset->addElement('submit', $this->getButtonName('submit'),
                              array('value' => 'Send!'));
        // The action to call if a user presses Enter rather than clicks on a button
        $this->setDefaultAction('submit');

        // Define filters and validation rules
        $name->addFilter('trim');
        $name->addRule('required', 'Please enter your name');
    }
}

// Action to process the form after successful validation
class TutorialProcess implements HTML_QuickForm2_Controller_Action
{
    public function perform(HTML_QuickForm2_Controller_Page $page, $name)
    {
        $values = $page->getController()->getValue();
        echo '<h1>Hello, ' . htmlspecialchars($values['name']) . '!</h1>';
    }
}

$page = new TutorialPage(new HTML_QuickForm2('tutorial'));
// We only add the custom 'process' handler, Controller will care for default ones
$page->addHandler('process', new TutorialProcess());

$controller = new HTML_QuickForm2_Controller('tutorial');
// Set defaults for the form elements
$controller->addDataSource(new HTML_QuickForm2_DataSource_Array(array(
    'name' => 'Joe User'
)));
$controller->addPage($page);
// Process the request
$controller->run();
?>