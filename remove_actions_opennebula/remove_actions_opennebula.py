from selenium import webdriver
import argparse


def cli():
    parser = argparse.ArgumentParser(description='Delete actions from OpenNebula VM.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument('-u', '--url', type=str, default='cloud.metacentrum.cz', help='URL to OpenNebula.')
    parser.add_argument('-p', '--protocol', type=str, default='https://', help='Web protocol.')
    parser.add_argument('-c', '--chromedriver', type=str, default='/usr/local/bin/chromedriver',
                        help='Path to chromedriver binary.')
    parser.add_argument('-a', '--actions', nargs='+', default=['terminate-hard'], help='Action types to remove.')
    parser.add_argument('username', type=str, help='OpenNebula username.')
    parser.add_argument('password', type=str, help='OpenNebula password.')
    parser.add_argument('vm_name', type=str, help='VM name.')

    args = vars(parser.parse_args())
    
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--window-size=1920,1080')

    driver = webdriver.Chrome(executable_path=args['chromedriver'], chrome_options=options)
    driver.get('{}{}:{}@{}'.format(args['protocol'], args['username'], args['password'], args['url']))

    if '401' in driver.title:
        print('Invalid credentials (error 401).')
        exit()

    print('Logged in!')

    driver.find_element_by_id('check_remember').click()
    driver.find_element_by_id('login_btn').click()

    driver.implicitly_wait(2)
    driver.find_element_by_id('li_instances-top-tab').find_element_by_tag_name('a').click()
    driver.implicitly_wait(2)
    driver.find_element_by_id('li_vms-tab').find_element_by_tag_name('a').click()
    driver.implicitly_wait(2)
    driver.find_element_by_css_selector('button[data-toggle="dataTableVmsSearch-dropdown"]').click()
    driver.find_element_by_css_selector('input[search-field="NAME"]').send_keys(args['vm_name'])
    driver.find_element_by_css_selector('input[search-field="UNAME"]').send_keys(args['username'])
    driver.find_element_by_css_selector('button.advanced-search').click()

    vm_table = driver.find_element_by_id('dataTableVms')
    if vm_table.find_element_by_css_selector('tbody tr:first-child td').text == 'No matching records found':
        print('No matching VMs found. Exiting...')
        exit()

    vm_table.find_element_by_css_selector('tbody tr:first-child').click()
    driver.find_element_by_id('vm_actions_tab-label').click()
    actions_table = driver.find_element_by_id('scheduling_actions_table')

    if actions_table.find_element_by_css_selector('tbody tr:first-child td').text == 'No actions to show':
        print('No actions for VM found. Exiting...')
        exit()

    found = False

    for action in actions_table.find_elements_by_css_selector('tbody tr'):
        el = action.find_element_by_css_selector('td.action_row')
        if el.text in args['actions']:
            print("Found '{}' action. Removing...".format(el.text))
            el.find_element_by_xpath('../td/div/a').click()
            found = True
            print('Done!')

    if not found:
        print('No matching actions ({}) were found'.format(args['actions']))


if __name__ == "__main__":
    cli()
